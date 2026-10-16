/**
 * `localStorage`-той аюулгүй ажиллах туслахууд.
 *
 * Шууд хандаж болохгүй хоёр шалтгаан:
 *   • Сервер дээр `window` байхгүй — render хийх үед унана.
 *   • Нууцлалын горим болон сайтын өгөгдөл хаасан тохиргоонд унших/бичих нь
 *     алдаа шиднэ. Тохиргоо алдагдсанаас хуудас унасан нь дор.
 *
 * Зөвхөн ХАРАГДАХ БАЙДЛЫН тохиргоонд ашиглана (хэсгийн өргөн, өндөр). Хэрэглэгчийн
 * ахиц, эрх зэрэг чухал өгөгдлийг backend баталгаажуулна.
 */

export function readLocal(key: string, fallback: string): string {
  if (typeof window === "undefined") return fallback;
  try {
    return window.localStorage.getItem(key) ?? fallback;
  } catch {
    return fallback;
  }
}

export function writeLocal(key: string, value: string): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // Хадгалж чадаагүй ч энэ удаагийн тохиргоо ажилласаар байна.
  }
}

/** Тоон утга уншина. Буруу утга хадгалагдсан бол анхдагчийг өгнө. */
export function readLocalNumber(key: string, fallback: number): number {
  const raw = readLocal(key, "");
  if (raw === "") return fallback;
  const value = Number.parseFloat(raw);
  return Number.isFinite(value) ? value : fallback;
}

/** `sessionStorage` — зөвхөн энэ таб, хаахад арилна. Алдааг `readLocal` шиг залгина. */
export function readSession(key: string, fallback: string): string {
  if (typeof window === "undefined") return fallback;
  try {
    return window.sessionStorage.getItem(key) ?? fallback;
  } catch {
    return fallback;
  }
}

export function writeSession(key: string, value: string): void {
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.setItem(key, value);
  } catch {
    // Хадгалж чадаагүй ч хуудас ажиллана.
  }
}
