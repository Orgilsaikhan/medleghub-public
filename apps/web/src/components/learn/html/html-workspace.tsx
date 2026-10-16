"use client";

import { BookOpenIcon, MonitorIcon, RotateCcwIcon } from "lucide-react";
import dynamic from "next/dynamic";
import { useCallback, useId, useMemo, useState, type ReactNode } from "react";

import { HtmlBrowserPane } from "@/components/learn/html/html-browser-pane";
import { FileTabs } from "@/components/learn/react/file-tabs";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { mn } from "@/lib/i18n/mn";
import { monacoLanguage, parseLessonFiles, type LessonFile } from "@/lib/sandbox/react/files";
import type { LessonLanguage } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const CodeEditor = dynamic(() => import("@/components/learn/code-editor"), {
  ssr: false,
  loading: () => <Skeleton className="h-full w-full rounded-none" />,
});

interface HtmlWorkspaceProps {
  lessonId: string;
  /** `html` — бүтцийн хичээл, `css` — загварын хичээл (эхлээд `style.css` нээгдэнэ). */
  language: LessonLanguage;
  initialCode: string;
  /** «Заавар» tab — хичээлийн текст, видео. */
  instructions: ReactNode;
  isDesktop: boolean;
}

type RightTab = "instructions" | "browser";
type MobileTab = "instructions" | "code" | "browser";

/**
 * HTML & CSS хичээлийн засварлагч — React хичээлийн байршилтай:
 *
 *     ┌ index.html │ style.css ──────── ↺ ┐ ┌ Заавар │ Хөтөч ─────────────┐
 *     │ засварлагч                       │ │ хичээл / таны хуудас         │
 *     └──────────────────────────────────┘ └─────────────────────────────┘
 *
 * «Хөтөч» нь код бичих зуур өөрөө шинэчлэгдэнэ — «Ажиллуулах» товчгүй.
 * Ctrl + Enter нь «Хөтөч»-ийг нээнэ. Нарийн дэлгэц дээр «Заавар / Код / Хөтөч».
 *
 * Хичээл солигдоход дуудагч `key`-г сольж component-ийг шинээр үүсгэнэ.
 */
export function HtmlWorkspace({
  lessonId,
  language,
  initialCode,
  instructions,
  isDesktop,
}: HtmlWorkspaceProps) {
  const isCss = language === "css";
  const initialFiles = useMemo(
    () => parseLessonFiles(initialCode, isCss ? "style.css" : "index.html"),
    [initialCode, isCss],
  );
  const [files, setFiles] = useState<LessonFile[]>(initialFiles);
  // CSS хичээлд загварын файлаас, HTML хичээлд хуудаснаас эхэлнэ.
  const [active, setActive] = useState(() => {
    const extension = isCss ? ".css" : ".html";
    const editable = initialFiles.filter((file) => !file.locked);
    return (
      editable.find((file) => file.name.endsWith(extension)) ??
      editable[0] ??
      initialFiles[0]
    ).name;
  });
  const activeFile = files.find((file) => file.name === active) ?? files[0];
  const idPrefix = useId().replace(/:/g, "");

  const [rightTab, setRightTab] = useState<RightTab>("instructions");
  const [mobileTab, setMobileTab] = useState<MobileTab>("instructions");
  const [confirmReset, setConfirmReset] = useState(false);
  // «Дахин эхлүүлэх» нь засварлагч, хөтөч хоёрыг шинээр үүсгэнэ: засварлагч
  // unmount болохдоо бүх файлын Monaco model-ийг устгадаг тул нээгээгүй
  // tab-ийн хуучин засвар үлдэхгүй; хөтөч эхний хуудас руугаа буцна.
  const [resetCount, setResetCount] = useState(0);

  const showBrowser = useCallback(() => {
    setRightTab("browser");
    setMobileTab("browser");
  }, []);

  // Tab солих үед Monaco шинэ model дээр `onChange` дуудаж болно — идэвхтэй
  // tab-аар биш, өөрчлөгдсөн model-ийн замаар шинэчилнэ (React-тай ижил).
  const modelScope = `/lesson-${lessonId}/`;
  const updateFile = useCallback(
    (code: string, modelPath?: string) => {
      if (!modelPath?.startsWith(modelScope)) return;
      const name = modelPath.slice(modelScope.length);
      setFiles((list) =>
        list.map((file) =>
          file.name === name && !file.locked && file.code !== code ? { ...file, code } : file,
        ),
      );
    },
    [modelScope],
  );

  const changed = files.some((file, index) => file.code !== initialFiles[index]?.code);

  const resetButton = (
    <Dialog open={confirmReset} onOpenChange={setConfirmReset}>
      <DialogTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={!changed}
          title={mn.learn.reset}
          aria-label={mn.learn.reset}
        >
          <RotateCcwIcon className="size-3.5" />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{mn.learn.reset}</DialogTitle>
          <DialogDescription>{mn.learn.resetConfirm}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setConfirmReset(false)}>
            {mn.admin.cancel}
          </Button>
          <Button
            variant="destructive"
            onClick={() => {
              setConfirmReset(false);
              setFiles(initialFiles);
              setResetCount((count) => count + 1);
            }}
          >
            {mn.learn.resetConfirmYes}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  const editor = (
    <div className="flex min-h-0 flex-1 flex-col">
      <FileTabs
        files={files}
        active={activeFile.name}
        onSelect={setActive}
        idPrefix={idPrefix}
        actions={resetButton}
      />
      <div
        id={`${idPrefix}-panel`}
        role="tabpanel"
        aria-labelledby={`${idPrefix}-tab-${files.indexOf(activeFile)}`}
        className="min-h-0 flex-1"
      >
        <CodeEditor
          key={resetCount}
          value={activeFile.code}
          onChange={updateFile}
          language={language}
          monacoLanguage={monacoLanguage(activeFile.name)}
          path={`${modelScope}${activeFile.name}`}
          modelScope={modelScope}
          readOnly={activeFile.locked}
          readOnlyMessage={mn.learn.react.lockedMessage}
          onRun={showBrowser}
        />
      </div>
    </div>
  );

  const browserPane = <HtmlBrowserPane key={resetCount} files={files} />;

  // Идэвхгүй tab-ийг `display:none` биш `invisible`-ээр нууна: iframe-ийн
  // хэмжээ зөв үлдэж, хуудас нь далд байхдаа ч шинэчлэгдсээр байна.
  const stacked = "absolute inset-0 data-[state=inactive]:invisible";

  if (!isDesktop) {
    return (
      <Tabs
        value={mobileTab}
        onValueChange={(value) => setMobileTab(value as MobileTab)}
        className="flex min-h-0 flex-1 flex-col gap-0"
      >
        <TabsList className="mx-3 mt-2 shrink-0 self-start">
          <TabsTrigger value="instructions">{mn.learn.react.instructions}</TabsTrigger>
          <TabsTrigger value="code">{mn.learn.react.code}</TabsTrigger>
          <TabsTrigger value="browser">{mn.learn.react.browser}</TabsTrigger>
        </TabsList>
        <div className="relative min-h-0 flex-1">
          <TabsContent value="instructions" forceMount className={stacked}>
            {instructions}
          </TabsContent>
          <TabsContent value="code" forceMount className={cn(stacked, "flex flex-col")}>
            {editor}
          </TabsContent>
          <TabsContent value="browser" forceMount className={stacked}>
            {browserPane}
          </TabsContent>
        </div>
      </Tabs>
    );
  }

  return (
    <div className="flex min-h-0 flex-1">
      <div className="flex min-h-0 w-1/2 min-w-0 flex-col border-r">{editor}</div>
      <Tabs
        value={rightTab}
        onValueChange={(value) => setRightTab(value as RightTab)}
        className="flex min-h-0 w-1/2 min-w-0 flex-col gap-0"
      >
        <TabsList variant="line" className="h-10 w-full shrink-0 justify-start border-b px-2">
          <TabsTrigger value="instructions" className="flex-none px-3">
            <BookOpenIcon aria-hidden />
            {mn.learn.react.instructions}
          </TabsTrigger>
          <TabsTrigger value="browser" className="flex-none px-3">
            <MonitorIcon aria-hidden />
            {mn.learn.react.browser}
          </TabsTrigger>
          <span className="text-muted-foreground ml-auto hidden truncate pr-1 text-xs xl:inline">
            {mn.learn.web.liveHint}
          </span>
        </TabsList>
        <div className="relative min-h-0 flex-1">
          <TabsContent value="instructions" forceMount className={stacked}>
            {instructions}
          </TabsContent>
          <TabsContent value="browser" forceMount className={stacked}>
            {browserPane}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
