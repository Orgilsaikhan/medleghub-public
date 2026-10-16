/**
 * Сурагчийн JSX-ийг хөтөч ойлгох JavaScript болгоно.
 *
 * 1. Acorn + acorn-jsx — синтаксийг шалгана. Sucrase нь хурдны тулд
 *    `<div>…</span>` мэт алдааг өнгөрөөдөг тул энэ алхам заавал хэрэгтэй.
 * 2. Sucrase — JSX болон `import`/`export`-ийг CommonJS болгоно. Мөрийн
 *    дугаарыг өөрчилдөггүй тул алдааны «App.jsx:12» зөв хэвээр үлдэнэ.
 * 3. Acorn — гарсан кодоос давталт бүрийг олж, биеийн эхэнд
 *    `__mhLoop()` шалгалт оруулна. Төгсгөлгүй давталт iframe-ийг (заримдаа
 *    хуудсыг бүхэлд нь) гацаахаас өмнө алдаа шидэж зогсооно.
 */

import { Parser, type Node } from "acorn";
import jsx from "acorn-jsx";
import { transform } from "sucrase";

import type { SandboxError } from "@/lib/sandbox/react/protocol";

export const LOOP_GUARD = "__mhLoop";

export class CompileError extends Error {
  constructor(readonly detail: SandboxError) {
    super(detail.message);
    this.name = "CompileError";
  }
}

interface Insertion {
  at: number;
  text: string;
}

const LOOPS = new Set([
  "ForStatement",
  "ForInStatement",
  "ForOfStatement",
  "WhileStatement",
  "DoWhileStatement",
]);

type AnyNode = Pick<Node, "type" | "start" | "end"> & { [key: string]: unknown };

function collectLoops(node: AnyNode, out: Insertion[]): void {
  if (LOOPS.has(node.type) && node.body) {
    const body = node.body as AnyNode;
    const check = `${LOOP_GUARD}();`;
    if (body.type === "BlockStatement") {
      out.push({ at: body.start + 1, text: check });
    } else {
      out.push({ at: body.start, text: `{${check}` });
      out.push({ at: body.end, text: "}" });
    }
  }
  for (const key of Object.keys(node)) {
    const value = node[key];
    if (Array.isArray(value)) {
      for (const child of value) {
        if (child && typeof child.type === "string") collectLoops(child as AnyNode, out);
      }
    } else if (value && typeof (value as AnyNode).type === "string") {
      collectLoops(value as AnyNode, out);
    }
  }
}

export function guardLoops(code: string): string {
  let ast: AnyNode;
  try {
    ast = Parser.parse(code, {
      ecmaVersion: "latest",
      sourceType: "script",
      allowReturnOutsideFunction: true,
      allowAwaitOutsideFunction: true,
      allowHashBang: true,
    }) as unknown as AnyNode;
  } catch {
    // Sucrase-ийн гаралт үргэлж зөв JavaScript. Хэрэв acorn ойлгохгүй бол
    // (шинэ синтакс) шалгалтгүйгээр ажиллуулна — алдаа хөтөч өөрөө хэлнэ.
    return code;
  }
  const insertions: Insertion[] = [];
  collectLoops(ast, insertions);
  insertions.sort((a, b) => b.at - a.at);
  let result = code;
  for (const { at, text } of insertions) {
    result = result.slice(0, at) + text + result.slice(at);
  }
  return result;
}

const JsxParser = Parser.extend(jsx());

/**
 * Түгээмэл синтакс алдааны монгол тайлбар. Эх англи мессежийг ХАМТ
 * үлдээнэ — бодит төсөлд яг ийм мессеж харна.
 */
const HINTS: [RegExp, (match: RegExpExecArray) => string][] = [
  [/Expected corresponding JSX closing tag for <([^>]*)>/, (m) => `<${m[1]}> шошгыг зөв хаагаагүй`],
  [
    /Adjacent JSX elements must be wrapped in an enclosing tag/,
    () => "JSX нэг л эх элемент буцаана — <div> эсвэл <>…</>-оор орооно уу",
  ],
  [/Unterminated JSX contents/, () => "JSX шошго хаагдаагүй байна"],
  [/Unterminated string constant/, () => "Хашилт хаагдаагүй байна"],
  [/Unterminated template/, () => "` хашилт хаагдаагүй байна"],
  [/Unexpected token/, () => "Энд байх ёсгүй тэмдэгт байна — хаалт, таслал, хашилтаа шалга"],
  [/Identifier '([^']+)' has already been declared/, (m) => `«${m[1]}» нэрийг хоёр удаа зарласан`],
  [/'return' outside of function/, () => "return нь функцийн гадна байна"],
  [/Unexpected keyword '([^']+)'/, (m) => `«${m[1]}» гэдэг үг энд байж болохгүй`],
];

function explain(message: string): string {
  for (const [pattern, hint] of HINTS) {
    const match = pattern.exec(message);
    if (match) return `${hint(match)} (${message})`;
  }
  return message;
}

/** «Unexpected token (3:10)» мессежээс байрлалыг салгана. */
function toCompileError(error: unknown, file: string): CompileError {
  const raw = error instanceof Error ? error.message : String(error);
  const match = /\((\d+):(\d+)\)\s*$/.exec(raw);
  const message = raw
    .replace(/^Error transforming [^:]+:\s*/, "")
    .replace(/\s*\(\d+:\d+\)\s*$/, "");
  return new CompileError({
    kind: "compile",
    message: explain(message),
    file,
    line: match ? Number(match[1]) : undefined,
    // Acorn, Sucrase хоёулаа баганыг 0-ээс тоолдог.
    column: match ? Number(match[2]) + 1 : undefined,
  });
}

/** Синтаксийг шалгана. Алдаа байвал `CompileError` шидэнэ. */
export function checkSyntax(code: string, file: string): void {
  try {
    JsxParser.parse(code, {
      ecmaVersion: "latest",
      sourceType: "module",
      allowAwaitOutsideFunction: true,
      allowHashBang: true,
    });
  } catch (error) {
    throw toCompileError(error, file);
  }
}

/** Сурагчийн модуль (`App.jsx`) — CommonJS болж `require` ашиглана. */
export function compileModule(code: string, file: string): string {
  if (file.endsWith(".json")) return `module.exports = ${code};`;
  checkSyntax(code, file);
  let output: string;
  try {
    output = transform(code, {
      transforms: ["jsx", "imports"],
      jsxRuntime: "automatic",
      production: false,
      filePath: file,
    }).code;
  } catch (error) {
    throw toCompileError(error, file);
  }
  return guardLoops(output);
}

/**
 * Дасгалын тест — async функцийн бие. `scope`-ийн нэрс (render, screen, …)
 * хувьсагч болж орно. Тест нь импорт бичдэггүй — `React`-ийг scope өгнө.
 */
export function compileTest(code: string, names: string[]): string {
  // Толгойг кодын эхний мөртэй НЭГ мөрөнд байлгаж мөрийн дугаарыг хадгална.
  const wrapped = `(async function (__scope) { const { ${names.join(", ")} } = __scope; ${code}\n})`;
  let output: string;
  try {
    output = transform(wrapped, {
      transforms: ["jsx"],
      jsxRuntime: "classic",
      production: true,
    }).code;
  } catch (error) {
    throw toCompileError(error, "test");
  }
  return guardLoops(output);
}
