"use client";

import { type RefObject, useEffect, useEffectEvent, useState, useSyncExternalStore } from "react";

import { useMediaQuery } from "@/lib/hooks/use-media-query";

/** Утасны хазайлт: нэгж тойрог дотор (|x|, |y| ≤ 1), 0 нь тайван байрлал. */
export type DeviceTilt = {
  /** Баруун тал нь доошилбол эерэг. */
  x: number;
  /** Дээд тал нь өргөгдөж утас босоо болбол эерэг. */
  y: number;
};

/** Хуруугаар удирддаг, hover-гүй төхөөрөмж — утас, таблет. */
const TOUCH_QUERY = "(hover: none) and (pointer: coarse)";
const REDUCED_MOTION_QUERY = "(prefers-reduced-motion: reduce)";

/** Ийм өнцгөөр (градус) хазайлгахад хазайлт ≈ 0.76 (tanh); цааш зөөлөн хязгаарлагдана. */
const RANGE_X = 15;
const RANGE_Y = 18;
/** Тэг байрлал шинэ өнцөгт аажмаар шилжинэ — утсыг яаж ч барьсан тайван үед 0 (мс). */
const RECENTER_MS = 4000;
/** Эхний уншилтууд тогтворгүй байж болно: энэ хугацаанд тэг хурдан тогтож, хариу аажмаар нэмэгдэнэ. */
const WARMUP_MS = 600;
const WARMUP_RECENTER_MS = 150;
/** Хөдөлгөөний зөөлрөлт (мс). */
const SMOOTH_MS = 120;
/** Хоёр уншилтын хоорондох ийм үсрэлт — өнцөг заагаа давсан тул тэгийг шинэчилнэ. */
const JUMP_DEG = 45;

const RAD = Math.PI / 180;

type Angles = { roll: number; pitch: number };
type Reading = Angles & { weight: number };
type PermissionRequest = () => Promise<PermissionState>;

/** Өнцгийн зөрүүг −180…180 болгоно. */
const wrap = (deg: number) => ((((deg + 180) % 360) + 360) % 360) - 180;

/**
 * `beta`, `gamma`-г дэлгэцийн тэнхлэгийн хазайлт болгоно. Эйлерийн өнцгийг
 * шууд хэрэглэвэл утсыг босоо барихад `gamma` огцом савладаг (gimbal lock),
 * тиймээс таталцлын чиглэлээр тооцно — тасралтгүй, луужингаас хамааралгүй.
 * Дэлгэц эргэсэн (landscape) бол тэнхлэгийг `screenAngle`-аар эргүүлнэ.
 */
function readTilt(beta: number, gamma: number, screenAngle: number): Reading {
  const b = beta * RAD;
  const g = gamma * RAD;
  const a = screenAngle * RAD;
  // «Дээш» чиглэл төхөөрөмжийн тэнхлэгт (x — баруун, y — дээд тал, z — дэлгэцээс гадагш).
  const ux = -Math.sin(g) * Math.cos(b);
  const uy = Math.sin(b);
  const uz = Math.cos(g) * Math.cos(b);
  // Дэлгэцийн тэнхлэгт: `angle` нь цагийн зүүний эсрэг эргэлт.
  const sx = ux * Math.cos(a) - uy * Math.sin(a);
  const sy = ux * Math.sin(a) + uy * Math.cos(a);
  return {
    roll: Math.asin(Math.max(-1, Math.min(1, -sx))) / RAD,
    pitch: Math.atan2(sy, uz) / RAD,
    // Утсыг хажуугаар нь барихад урд/хойш хазайлт тодорхойгүй болно — жинг багасгана.
    weight: Math.hypot(sy, uz),
  };
}

/**
 * `DeviceOrientationEvent.requestPermission` — iOS 13+ Safari, Chrome 151+.
 * Chrome мэдрэгчийг анхнаасаа зөвшөөрдөг тул товшилтгүйгээр «granted» буцаана.
 */
function permissionRequest(): PermissionRequest | null {
  if (typeof DeviceOrientationEvent === "undefined") return null;
  const request = (DeviceOrientationEvent as unknown as { requestPermission?: PermissionRequest })
    .requestPermission;
  return typeof request === "function" ? () => request.call(DeviceOrientationEvent) : null;
}

const subscribeNever = () => () => {};

/**
 * Утасны хазайлтыг (`deviceorientation`) дагана — hero-гийн 3D цонх утсыг
 * хөдөлгөхөд эргэнэ.
 *
 * Зөвхөн hover-гүй мэдрэгч дэлгэцтэй төхөөрөмжид, `ref` элемент дэлгэц дээр
 * харагдаж, таб идэвхтэй үед сонсоно; хөдөлгөөн багасгах тохиргоотой бол
 * огт ажиллахгүй. Эхний уншилт нь тэг байрлал бөгөөд хэдэн секундэд аажмаар
 * шинэчлэгдэнэ. Утгыг кадр бүрт (requestAnimationFrame) зөөлрүүлж `onTilt`-д
 * өгнө (React state биш); сонсохоо болиход `onTilt(null)`. Мэдрэгчгүй
 * төхөөрөмжид үйл явдал ирэхгүй тул юу ч өөрчлөгдөхгүй.
 *
 * iOS Safari зөвшөөрлийг зөвхөн хэрэглэгчийн товшилтоор асуудаг:
 * `needsPermission` үед товч харуулж, дарахад нь `requestPermission`-ийг дуудна.
 */
export function useDeviceTilt(
  ref: RefObject<HTMLElement | null>,
  onTilt: (tilt: DeviceTilt | null) => void,
) {
  const touch = useMediaQuery(TOUCH_QUERY);
  const reducedMotion = useMediaQuery(REDUCED_MOTION_QUERY);
  const enabled = touch && !reducedMotion;
  // Зөвшөөрлийн API байгаа эсэх (сервер дээр болон hydration-ийн үед — үгүй).
  const askable = useSyncExternalStore(
    subscribeNever,
    () => permissionRequest() !== null,
    () => false,
  );
  const [permission, setPermission] = useState<PermissionState | null>(null);
  const emit = useEffectEvent(onTilt);

  // Товшилтгүйгээр асууна: Chrome болон энэ session-д аль хэдийн шийдсэн iOS шууд
  // хариулна. iOS шийдээгүй бол `NotAllowedError`-оор татгалзана (юу ч хадгалахгүй)
  // — тэр үед товч харуулна.
  useEffect(() => {
    const request = permissionRequest();
    if (!enabled || !request) return;
    let alive = true;
    request().then(
      (state) => {
        if (alive) setPermission(state);
      },
      (error: unknown) => {
        if (!alive) return;
        const needsGesture = error instanceof DOMException && error.name === "NotAllowedError";
        setPermission(needsGesture ? "prompt" : "denied");
      },
    );
    return () => {
      alive = false;
    };
  }, [enabled]);

  const active = enabled && (!askable || permission === "granted");

  useEffect(() => {
    const element = ref.current;
    if (!active || !element) return;

    let reading: Reading | null = null;
    let base: Angles | null = null;
    let screenAngle = 0;
    let startedAt = 0;
    let last = 0;
    let frame = 0;
    let listening = false;
    const tilt = { x: 0, y: 0 };
    const shown = { x: 0, y: 0 };

    const step = (now: number) => {
      frame = 0;
      if (!reading) return;
      const dt = Math.min(now - last, 100);
      last = now;
      if (!base) {
        base = { roll: reading.roll, pitch: reading.pitch };
        startedAt = now;
      }
      const warm = Math.min(1, (now - startedAt) / WARMUP_MS);
      const follow = 1 - Math.exp(-dt / (warm < 1 ? WARMUP_RECENTER_MS : RECENTER_MS));
      base.roll += (reading.roll - base.roll) * follow;
      base.pitch += wrap(reading.pitch - base.pitch) * follow;

      const roll = reading.roll - base.roll;
      const pitch = wrap(reading.pitch - base.pitch);
      // Дугуй хязгаар: хоёр тийш зэрэг хазайлгахад булангаар хэт гарахгүй.
      const rawX = roll / RANGE_X;
      const rawY = (pitch / RANGE_Y) * reading.weight;
      const radius = Math.hypot(rawX, rawY);
      const scale = (radius > 1e-6 ? Math.tanh(radius) / radius : 1) * warm;
      const targetX = rawX * scale;
      const targetY = rawY * scale;
      const ease = 1 - Math.exp(-dt / SMOOTH_MS);
      tilt.x += (targetX - tilt.x) * ease;
      tilt.y += (targetY - tilt.y) * ease;

      // Үл мэдэгдэх өөрчлөлтөөр (мэдрэгчийн чичиргээ, ~0.1°) хуудсыг дахин зуруулахгүй.
      if (Math.abs(tilt.x - shown.x) > 0.008 || Math.abs(tilt.y - shown.y) > 0.008) {
        shown.x = tilt.x;
        shown.y = tilt.y;
        emit({ x: tilt.x, y: tilt.y });
      }
      // Тайвширсан бол зогсоно; дараагийн уншилт дахин эхлүүлнэ.
      const settling =
        Math.abs(targetX - tilt.x) + Math.abs(targetY - tilt.y) > 0.001 ||
        Math.abs(roll) + Math.abs(pitch) > 0.1;
      if (settling) frame = requestAnimationFrame(step);
    };

    const onOrientation = (event: DeviceOrientationEvent) => {
      if (event.beta === null || event.gamma === null) return;
      const angle = screen.orientation?.angle ?? window.orientation ?? 0;
      const next = readTilt(event.beta, event.gamma, angle);
      // Дэлгэц эргэсэн эсвэл өнцөг үсэрсэн бол шинэ байрлалаас эхэлнэ — огцом савлахгүй.
      const jumped =
        reading !== null &&
        (angle !== screenAngle ||
          Math.abs(next.roll - reading.roll) > JUMP_DEG ||
          Math.abs(wrap(next.pitch - reading.pitch)) > JUMP_DEG);
      if (jumped && base) base = { roll: next.roll, pitch: next.pitch };
      screenAngle = angle;
      reading = next;
      if (!frame) {
        last = performance.now();
        frame = requestAnimationFrame(step);
      }
    };

    const start = () => {
      if (listening) return;
      listening = true;
      window.addEventListener("deviceorientation", onOrientation);
    };

    const stop = () => {
      if (!listening) return;
      listening = false;
      window.removeEventListener("deviceorientation", onOrientation);
      cancelAnimationFrame(frame);
      frame = 0;
      reading = null;
      base = null;
      tilt.x = 0;
      tilt.y = 0;
      shown.x = 0;
      shown.y = 0;
      emit(null);
    };

    // Дэлгэцэн дээр харагдаж, таб идэвхтэй үед л сонсоно.
    let onScreen = false;
    const sync = () => (onScreen && document.visibilityState === "visible" ? start() : stop());
    const observer = new IntersectionObserver((entries) => {
      // Нэг дуудлагад хэд хэдэн бичлэг ирж болно — сүүлийнх нь одоогийн төлөв.
      onScreen = entries.at(-1)?.isIntersecting ?? false;
      sync();
    });
    observer.observe(element);
    document.addEventListener("visibilitychange", sync);
    return () => {
      observer.disconnect();
      document.removeEventListener("visibilitychange", sync);
      stop();
    };
  }, [active, ref]);

  const requestPermission = () => {
    const request = permissionRequest();
    if (!request) return;
    // Товшилтын дотор шууд дуудна — эс бөгөөс iOS асуухгүй. «granted»-аас бусад
    // хариуд товч нуугдана (дахин дахин гарахгүй).
    request().then(
      (state) => setPermission(state === "granted" ? "granted" : "denied"),
      () => setPermission("denied"),
    );
  };

  return {
    /** Хөдөлгөөн мэдрэгчийг зөвшөөрөх товч харуулах үе (iOS). */
    needsPermission: enabled && askable && permission === "prompt",
    requestPermission,
  };
}
