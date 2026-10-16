"use client";

import { ArrowLeftIcon, ArrowRightIcon, RotateCwIcon } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import type { SandboxJob, SandboxMessage } from "@/lib/sandbox/react/protocol";
import { mountSandbox, SANDBOX_PERMISSIONS, sendCommand } from "@/lib/sandbox/react/runner";

export interface BrowserState {
  title: string;
  path: string;
  canGoBack: boolean;
  canGoForward: boolean;
}

export const INITIAL_BROWSER: BrowserState = {
  title: "React App",
  path: "/",
  canGoBack: false,
  canGoForward: false,
};

interface BrowserPaneProps {
  job: SandboxJob;
  state: BrowserState;
  onMessage: (message: SandboxMessage) => void;
  onReload: () => void;
}

/** Хаягийн мөрөнд харагдах хост — Vite-ийн хөгжүүлэлтийн сервер шиг. */
const HOST = "localhost:5173";

/**
 * «Хөтөч» — сурагчийн апп sandbox iframe дотор. Дээд талын мөр нь жинхэнэ
 * хөтөч шиг: буцах/урагшлах (react-router-тэй үед), дахин ачаалах, хаяг,
 * `document.title`.
 */
export function BrowserPane({ job, state, onMessage, onReload }: BrowserPaneProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const handlerRef = useRef(onMessage);
  useEffect(() => {
    handlerRef.current = onMessage;
  }, [onMessage]);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    return mountSandbox(iframe, job, (message) => handlerRef.current(message));
  }, [job]);

  // Хаягийн мөрийг гараар засаж болно — Enter дарахад тэр зам руу шилжинэ.
  const [draft, setDraft] = useState<string | null>(null);
  const address = draft ?? state.path;

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="bg-muted/60 flex shrink-0 items-center gap-1 border-b px-2 py-1.5">
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={!state.canGoBack}
          onClick={() => sendCommand(iframeRef.current, { type: "navigate", to: "back" })}
          aria-label={mn.learn.react.back}
          title={mn.learn.react.back}
        >
          <ArrowLeftIcon className="size-3.5" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={!state.canGoForward}
          onClick={() => sendCommand(iframeRef.current, { type: "navigate", to: "forward" })}
          aria-label={mn.learn.react.forward}
          title={mn.learn.react.forward}
        >
          <ArrowRightIcon className="size-3.5" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          onClick={onReload}
          aria-label={mn.learn.react.reload}
          title={mn.learn.react.reload}
        >
          <RotateCwIcon className="size-3.5" />
        </Button>
        <form
          className="min-w-0 flex-1"
          onSubmit={(event) => {
            event.preventDefault();
            const path = address.replace(/^https?:\/\/[^/]+/, "") || "/";
            sendCommand(iframeRef.current, { type: "navigate", to: "path", path });
            setDraft(null);
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
          className="text-muted-foreground hidden max-w-40 truncate text-xs xl:inline"
          title={state.title}
        >
          {state.title}
        </span>
      </div>
      {/* Сурагчийн хуудас жинхэнэ хөтөч шиг цагаан дэвсгэртэй — өөрийн CSS-ээ
          бичнэ. Сайтын бараан горим энд нөлөөлөхгүй. */}
      <iframe
        ref={iframeRef}
        title={mn.learn.react.frameTitle}
        sandbox={SANDBOX_PERMISSIONS}
        className="min-h-0 w-full flex-1 border-0 bg-white"
      />
    </div>
  );
}
