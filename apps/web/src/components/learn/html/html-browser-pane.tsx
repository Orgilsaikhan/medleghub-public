"use client";

import {
  ArrowLeftIcon,
  ArrowRightIcon,
  ExternalLinkIcon,
  MonitorIcon,
  RotateCwIcon,
  SmartphoneIcon,
  TabletIcon,
  XIcon,
} from "lucide-react";
import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import {
  buildPreview,
  homePage,
  isPageFile,
  PREVIEW_PERMISSIONS,
  readPreviewMessage,
  resolvePath,
  sendStyle,
  type PreviewMessage,
} from "@/lib/sandbox/html/preview";
import type { LessonFile } from "@/lib/sandbox/react/files";
import { cn } from "@/lib/utils";

/** Хаягийн мөрөнд — VS Code-ийн Live Server-ийн хаяг, сурагчдад танил. */
const HOST = "127.0.0.1:5500/";

/** HTML өөрчлөгдвөл хуудас дахин ачаална — бичиж дуусахыг бага зэрэг хүлээнэ. */
const HTML_DELAY_MS = 400;
/** CSS нь дахин ачаалалгүй солигдох тул бараг шууд. */
const CSS_DELAY_MS = 120;

const DEVICES = {
  phone: { width: 375, icon: SmartphoneIcon, label: mn.learn.web.devicePhone },
  tablet: { width: 768, icon: TabletIcon, label: mn.learn.web.deviceTablet },
  full: { width: null, icon: MonitorIcon, label: mn.learn.web.deviceFull },
} as const;
type Device = keyof typeof DEVICES;

type Notice =
  | { kind: "external"; url: string }
  | { kind: "missing"; href: string }
  | { kind: "app"; href: string }
  | { kind: "submit"; request: string; fields: [string, string][] }
  | { kind: "alert"; text: string };

interface Built {
  runId: number;
  page: string;
  reload: number;
  html: string | undefined;
  /** `<style>` болж орсон CSS файл → тэр үеийн агуулга. */
  styles: Map<string, string>;
  /** Iframe доторх script ажиллаж эхэлсэн — CSS-ийг мессежээр сольж болно. */
  ready: boolean;
}

let runCounter = 0;

function codeOf(files: LessonFile[], name: string): string {
  return files.find((file) => file.name === name)?.code ?? "";
}

/**
 * HTML & CSS хичээлийн «Хөтөч». Код өөрчлөгдөхөд өөрөө шинэчлэгдэнэ:
 * HTML засвар хуудсыг дахин ачаална (гүйлгэсэн байрлал хадгалагдана), CSS
 * засвар `<style>`-ийг шууд сольно.
 *
 * Дээд мөр нь жинхэнэ хөтөч шиг: буцах/урагшлах (хуудас хооронд), дахин
 * ачаалах, хаяг (`tuhai.html` бичээд Enter), `<title>`, дэлгэцийн өргөн
 * (утас, таблет — хариуцлагатай дизайны хичээлд).
 */
export function HtmlBrowserPane({ files }: { files: LessonFile[] }) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [history, setHistory] = useState(() => {
    const home = homePage(files);
    return { pages: home ? [home] : [], index: 0 };
  });
  const page = history.pages[history.index] ?? null;
  const [reload, setReload] = useState(0);
  const [title, setTitle] = useState("");
  const [notice, setNotice] = useState<Notice | null>(null);
  const [device, setDevice] = useState<Device>("full");
  const [width, setWidth] = useState<number | null>(null);
  const [draft, setDraft] = useState<string | null>(null);

  const built = useRef<Built | null>(null);
  const scrollY = useRef(0);
  const pendingHash = useRef("");

  const navigate = useCallback((target: string, hash = "") => {
    pendingHash.current = hash;
    scrollY.current = 0;
    setNotice(null);
    setHistory((state) =>
      state.pages[state.index] === target
        ? state
        : { pages: [...state.pages.slice(0, state.index + 1), target], index: state.index + 1 },
    );
    // Ижил хуудасны `#id` руу ч дахин ачаална.
    setReload((count) => count + 1);
  }, []);

  const go = (step: -1 | 1) => {
    scrollY.current = 0;
    pendingHash.current = "";
    setNotice(null);
    setHistory((state) => ({
      ...state,
      index: Math.min(Math.max(state.index + step, 0), state.pages.length - 1),
    }));
  };

  // --- Хуудсыг шинэчлэх ---------------------------------------------------------

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe || !page) return;
    const html = files.find((file) => file.name === page)?.code;
    const previous = built.current;

    const rebuild = () => {
      runCounter += 1;
      const result = buildPreview(files, page, {
        runId: runCounter,
        scrollY: scrollY.current,
        hash: pendingHash.current,
      });
      pendingHash.current = "";
      built.current = {
        runId: runCounter,
        page,
        reload,
        html,
        styles: new Map(result.styles.map((name) => [name, codeOf(files, name)])),
        ready: false,
      };
      iframe.srcdoc = result.srcdoc;
    };

    // Шинэ хуудас, «Дахин ачаалах» — шууд. HTML засвар — бичиж дуусахыг хүлээнэ.
    if (!previous || previous.page !== page || previous.reload !== reload) {
      rebuild();
      return;
    }
    if (previous.html !== html) {
      const timer = window.setTimeout(rebuild, HTML_DELAY_MS);
      return () => window.clearTimeout(timer);
    }

    const changed = [...previous.styles.keys()].filter(
      (name) => codeOf(files, name) !== previous.styles.get(name),
    );
    if (changed.length === 0) return;
    const timer = window.setTimeout(() => {
      // Хуудас ачаалагдаж дуусаагүй бол мессеж хуучин хуудсанд очиж болно.
      if (!previous.ready) return rebuild();
      for (const name of changed) {
        const code = codeOf(files, name);
        previous.styles.set(name, code);
        sendStyle(iframe, name, code);
      }
    }, CSS_DELAY_MS);
    return () => window.clearTimeout(timer);
  }, [files, page, reload]);

  // --- Iframe-ийн мессеж --------------------------------------------------------------

  const openLink = useCallback(
    (href: string, from: string) => {
      const target = resolvePath(href, from);
      if (target) {
        if (isPageFile(target.path) && files.some((file) => file.name === target.path)) {
          navigate(target.path, target.hash);
        } else {
          setNotice({ kind: "missing", href });
        }
        return;
      }
      const scheme = /^([a-z][a-z\d+.-]*):/i.exec(href.trim())?.[1]?.toLowerCase();
      if (scheme === "javascript") return;
      if (scheme === "mailto" || scheme === "tel" || scheme === "sms") {
        setNotice({ kind: "app", href });
        return;
      }
      try {
        const url = new URL(href.trim(), "https://example.com");
        if (url.protocol === "http:" || url.protocol === "https:") {
          setNotice({ kind: "external", url: url.href });
          return;
        }
      } catch {
        // Буруу хаяг — доор «олдсонгүй».
      }
      setNotice({ kind: "missing", href });
    },
    [files, navigate],
  );

  const onMessage = useCallback(
    (message: PreviewMessage) => {
      switch (message.type) {
        case "title":
          if (built.current) built.current.ready = true;
          setTitle(message.title);
          break;
        case "scroll":
          scrollY.current = message.y;
          break;
        case "link":
          if (page) openLink(message.href, page);
          break;
        case "alert":
          setNotice({ kind: "alert", text: message.text });
          break;
        case "submit": {
          const action = message.action.trim() || page || "";
          setNotice({
            kind: "submit",
            request: `${message.method.toUpperCase()} ${action}`,
            fields: message.fields,
          });
          break;
        }
      }
    },
    [openLink, page],
  );

  useEffect(() => {
    const listener = (event: MessageEvent) => {
      const iframe = iframeRef.current;
      const current = built.current;
      if (!iframe || !current || event.source !== iframe.contentWindow) return;
      const message = readPreviewMessage(event.data, current.runId);
      if (message) onMessage(message);
    };
    window.addEventListener("message", listener);
    return () => window.removeEventListener("message", listener);
  }, [onMessage]);

  // Хариуцлагатай дизайнд: одоогийн өргөнийг пикселээр харуулна.
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    const observer = new ResizeObserver(([entry]) => setWidth(Math.round(entry.contentRect.width)));
    observer.observe(iframe);
    return () => observer.disconnect();
  }, []);

  const address = draft ?? page ?? "";
  const deviceWidth = DEVICES[device].width;

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="bg-muted/60 @container flex shrink-0 items-center gap-1 border-b px-2 py-1.5">
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={history.index === 0}
          onClick={() => go(-1)}
          aria-label={mn.learn.react.back}
          title={mn.learn.react.back}
        >
          <ArrowLeftIcon className="size-3.5" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={history.index >= history.pages.length - 1}
          onClick={() => go(1)}
          aria-label={mn.learn.react.forward}
          title={mn.learn.react.forward}
        >
          <ArrowRightIcon className="size-3.5" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={!page}
          onClick={() => {
            setNotice(null);
            setReload((count) => count + 1);
          }}
          aria-label={mn.learn.react.reload}
          title={mn.learn.react.reload}
        >
          <RotateCwIcon className="size-3.5" />
        </Button>
        <form
          className="min-w-0 flex-1"
          onSubmit={(event) => {
            event.preventDefault();
            setDraft(null);
            const value = address.trim().replace(/^(https?:\/\/)?127\.0\.0\.1:5500\/?/i, "");
            const hasScheme = /^[a-z][a-z\d+.-]*:/i.test(value);
            openLink(hasScheme ? value : `/${value.replace(/^\/+/, "")}`, page ?? "index.html");
          }}
        >
          <label className="bg-background focus-within:ring-ring flex h-7 items-center rounded-full border px-3 font-mono text-xs focus-within:ring-2">
            <span className="sr-only">{mn.learn.react.address}</span>
            <span className="text-muted-foreground shrink-0">{HOST}</span>
            <input
              value={address}
              onChange={(event) => setDraft(event.target.value)}
              onBlur={() => setDraft(null)}
              spellCheck={false}
              className="min-w-0 flex-1 bg-transparent outline-none"
            />
          </label>
        </form>
        <span
          className="text-muted-foreground hidden max-w-40 truncate text-xs @3xl:inline"
          title={title}
        >
          {title}
        </span>
        {width !== null && (
          <span
            className="text-muted-foreground hidden font-mono text-[11px] tabular-nums @lg:inline"
            title={mn.learn.web.viewportWidth}
          >
            {width}px
          </span>
        )}
        <div role="group" aria-label={mn.learn.web.viewport} className="hidden @md:flex">
          {(Object.keys(DEVICES) as Device[]).map((key) => {
            const { icon: Icon, label } = DEVICES[key];
            return (
              <Button
                key={key}
                variant="ghost"
                size="icon"
                className={cn("size-7", device === key && "bg-background shadow-xs")}
                aria-pressed={device === key}
                aria-label={label}
                title={label}
                onClick={() => setDevice(key)}
              >
                <Icon className="size-3.5" />
              </Button>
            );
          })}
        </div>
      </div>

      <div className="relative min-h-0 flex-1">
        <div
          className={cn(
            "flex h-full justify-center overflow-auto",
            deviceWidth !== null && "bg-muted/40",
          )}
        >
          {/* Сурагчийн хуудас жинхэнэ хөтөч шиг цагаан дэвсгэртэй. */}
          <iframe
            ref={iframeRef}
            title={mn.learn.web.frameTitle}
            sandbox={PREVIEW_PERMISSIONS}
            className={cn("h-full shrink-0 border-0 bg-white", !page && "invisible")}
            style={{ width: deviceWidth === null ? "100%" : `${deviceWidth}px` }}
          />
        </div>

        {!page && (
          <p className="text-muted-foreground absolute inset-0 grid place-items-center p-6 text-center text-sm">
            {mn.learn.web.noPage}
          </p>
        )}

        {/* Үргэлж байх `aria-live` — шинэ мэдэгдлийг дэлгэц уншигч хэлнэ. */}
        <div
          aria-live="polite"
          className="pointer-events-none absolute inset-x-2 bottom-2 flex justify-center"
        >
          {notice && <NoticeCard notice={notice} onClose={() => setNotice(null)} />}
        </div>
      </div>
    </div>
  );
}

function NoticeCard({ notice, onClose }: { notice: Notice; onClose: () => void }) {
  const t = mn.learn.web;
  let heading: string;
  let body: ReactNode;
  switch (notice.kind) {
    case "external":
      heading = t.externalTitle;
      body = (
        <>
          <p className="text-muted-foreground">{t.externalText}</p>
          <p className="mt-1 font-mono text-xs break-all">{notice.url}</p>
          <a
            href={notice.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand-link mt-2 inline-flex items-center gap-1 font-medium underline-offset-4 hover:underline"
          >
            {t.externalOpen}
            <ExternalLinkIcon className="size-3.5" aria-hidden />
          </a>
        </>
      );
      break;
    case "missing":
      heading = t.missingTitle;
      body = <p className="text-muted-foreground break-words">{t.missingText(notice.href)}</p>;
      break;
    case "app":
      heading = t.appLinkTitle;
      body = <p className="text-muted-foreground break-words">{t.appLinkText(notice.href)}</p>;
      break;
    case "submit":
      heading = t.submitTitle;
      body = (
        <>
          <p className="text-muted-foreground">{t.submitText}</p>
          <p className="mt-1 font-mono text-xs break-all">{notice.request}</p>
          {notice.fields.length === 0 ? (
            <p className="text-muted-foreground mt-1 text-xs">{t.submitEmpty}</p>
          ) : (
            <dl className="mt-1.5 grid max-h-32 grid-cols-[auto_1fr] gap-x-3 gap-y-0.5 overflow-y-auto font-mono text-xs">
              {notice.fields.map(([name, value], index) => (
                <div key={index} className="contents">
                  <dt className="text-muted-foreground">{name}</dt>
                  <dd className="min-w-0 break-all">{value || "—"}</dd>
                </div>
              ))}
            </dl>
          )}
        </>
      );
      break;
    case "alert":
      heading = t.alertTitle;
      body = <p className="break-words whitespace-pre-wrap">{notice.text}</p>;
      break;
  }

  return (
    <div className="bg-popover text-popover-foreground pointer-events-auto w-full max-w-md rounded-lg border p-3 text-sm shadow-lg">
      <div className="flex items-start gap-2">
        <div className="min-w-0 flex-1">
          <p className="font-medium">{heading}</p>
          <div className="mt-0.5">{body}</div>
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="-mt-1 -mr-1 size-7"
          onClick={onClose}
          aria-label={t.close}
          title={t.close}
        >
          <XIcon className="size-3.5" />
        </Button>
      </div>
    </div>
  );
}
