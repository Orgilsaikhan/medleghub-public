"use client";

import Editor, { type OnMount } from "@monaco-editor/react";
import { useTheme } from "next-themes";
import { useCallback, useEffect, useRef } from "react";

import { configureMonaco } from "@/components/learn/monaco-loader";
import { Skeleton } from "@/components/ui/skeleton";
import type { LessonLanguage } from "@/lib/types/api";

interface CodeEditorProps {
  value: string;
  /**
   * `modelPath` — өөрчлөгдсөн model-ийн зам. Олон файлтай засварлагчид tab
   * солих үед `@monaco-editor/react` шинэ model дээр `onChange` дуудаж
   * болох тул «идэвхтэй файл»-аар биш замаар нь шинэчилнэ.
   */
  onChange: (value: string, modelPath?: string) => void;
  language: LessonLanguage;
  /** Ctrl/Cmd + Enter дарахад ажиллана. */
  onRun?: () => void;
  /**
   * Олон файлтай хичээл (React): файл бүр өөрийн model-той — undo түүх
   * хадгалагдана. `.jsx`-ээр төгссөн зам нь Monaco-д JSX-ийг танина.
   */
  path?: string;
  /** Файлын төрлөөр — `html`, `css`, `javascript`. Өгөөгүй бол `language`. */
  monacoLanguage?: string;
  readOnly?: boolean;
  readOnlyMessage?: string;
  /**
   * Энэ угтвартай бүх model-ийг unmount үед устгана. Хичээл рүү буцаж ирэхэд
   * өмнөх засвар биш анхны код харагдана.
   */
  modelScope?: string;
}

type MonacoInstance = Parameters<OnMount>[1];

/**
 * Monaco 0.5x нь TypeScript-ийн API-г `monaco.typescript` руу зөөсөн.
 * Хуучин `languages.typescript` нь ажиллах хугацаанд хэвээр байж болох тул
 * аль байгааг нь ашиглана.
 */
function typescriptApi(monaco: MonacoInstance) {
  const api = monaco as unknown as {
    typescript?: TypeScriptApi;
    languages: { typescript?: TypeScriptApi };
  };
  const candidate = api.typescript ?? api.languages.typescript;
  return candidate && "javascriptDefaults" in candidate ? candidate : null;
}

interface TypeScriptApi {
  javascriptDefaults: {
    setDiagnosticsOptions: (options: object) => void;
    setCompilerOptions: (options: object) => void;
  };
  JsxEmit: { Preserve: number };
  ScriptTarget: { ESNext: number };
}

/**
 * Monaco засварлагч.
 *
 * `lesson-editor.tsx` дотор lazy ачаалагдана. Код нь зөвхөн browser-ийн
 * санах ойд байх бөгөөд сервер рүү илгээгддэггүй.
 */
// Модул ачаалагдахад л тохируулна — Editor render хийхээс өмнө биелэх ёстой.
configureMonaco();

export default function CodeEditor({
  value,
  onChange,
  language,
  onRun,
  path,
  monacoLanguage,
  readOnly = false,
  readOnlyMessage,
  modelScope,
}: CodeEditorProps) {
  const { resolvedTheme } = useTheme();

  // Товчлолын callback нь Monaco-д нэг л удаа бүртгэгддэг тул хамгийн сүүлийн
  // хувилбарыг ref-ээр дамжуулна (render-ийн үед ref-д хандахгүй).
  const runRef = useRef(onRun);
  useEffect(() => {
    runRef.current = onRun;
  }, [onRun]);

  const monacoRef = useRef<MonacoInstance | null>(null);
  const editorRef = useRef<Parameters<OnMount>[0] | null>(null);
  useEffect(() => {
    if (!modelScope) return;
    return () => {
      const monaco = monacoRef.current;
      if (!monaco) return;
      for (const model of monaco.editor.getModels()) {
        if (model.uri.path.startsWith(modelScope)) model.dispose();
      }
    };
  }, [modelScope]);

  const handleMount: OnMount = useCallback((editor, monaco) => {
    monacoRef.current = monaco;
    editorRef.current = editor;
    // Гараас гаргалгүй кодоо ажиллуулах товчлол.
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => runRef.current?.());

    const typescript = typescriptApi(monaco);
    // Хичээлийн код нь бүтэн төсөл биш тул модулын алдаа заахгүй.
    typescript?.javascriptDefaults.setDiagnosticsOptions({
      noSemanticValidation: true,
      noSyntaxValidation: false,
    });
    // `.jsx` файлд JSX-ийг синтакс алдаа гэж заахгүй. Энгийн `.js` model-д
    // (JavaScript сургалт) нөлөөгүй — JSX-ийг зөвхөн `.jsx` файлд задалдаг.
    typescript?.javascriptDefaults.setCompilerOptions({
      allowJs: true,
      allowNonTsExtensions: true,
      jsx: typescript.JsxEmit.Preserve,
      target: typescript.ScriptTarget.ESNext,
    });
  }, []);

  return (
    <Editor
      value={value}
      path={path}
      language={monacoLanguage ?? (language === "jsx" ? "javascript" : language)}
      onChange={(next) => onChange(next ?? "", editorRef.current?.getModel()?.uri.path)}
      onMount={handleMount}
      // Код бичих талбар нь хоёр темад ч бараан — редакторын уламжлалт мэдрэмж.
      theme={resolvedTheme === "light" ? "vs" : "vs-dark"}
      loading={<Skeleton className="h-full w-full rounded-none" />}
      options={{
        fontSize: 14,
        fontFamily: "var(--font-geist-mono), ui-monospace, monospace",
        lineHeight: 1.7,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        automaticLayout: true,
        tabSize: 2,
        renderLineHighlight: "line",
        smoothScrolling: true,
        padding: { top: 14, bottom: 14 },
        scrollbar: { verticalScrollbarSize: 10, horizontalScrollbarSize: 10 },
        wordWrap: "on",
        // Enter нь ҮРГЭЛЖ шинэ мөр үүсгэнэ. Анхдагчаар Monaco нь Enter дарахад
        // санал болгосон үгийг оруулдаг бөгөөд энэ нь шинэ суралцагчийн бичсэн
        // кодыг гэнэт өөрчилдөг. Саналыг Tab-аар хүлээж авна.
        acceptSuggestionOnEnter: "off",
        acceptSuggestionOnCommitCharacter: false,
        tabCompletion: "on",
        quickSuggestions: { other: true, comments: false, strings: false },
        // Суралцагчийг төөрөгдүүлэхгүйн тулд нэмэлт чимэглэлийг багасгав.
        folding: false,
        glyphMargin: false,
        lineNumbersMinChars: 3,
        overviewRulerLanes: 0,
        contextmenu: false,
        readOnly,
        readOnlyMessage: readOnlyMessage ? { value: readOnlyMessage } : undefined,
        // Кирилл «у», «о», «с» нь латин үсэгтэй адил харагддаг тул Monaco
        // монгол текст бүрийг «төөрөгдүүлэх тэмдэгт» гэж хүрээлдэг.
        unicodeHighlight: { ambiguousCharacters: false, invisibleCharacters: true },
      }}
    />
  );
}
