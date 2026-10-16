/**
 * Жижиг CommonJS модулийн систем — Vite-ийн оронд.
 *
 * `import App from "./App"` нь Sucrase-ийн дараа `require("./App")` болно.
 * Энд тэр дуудлагыг сурагчийн файл (`App.jsx`) эсвэл бэлэн сан (`react`,
 * `react-router`, …) руу холбоно.
 *
 * Хөрвүүлэлтийг файлын агуулгаар кэшлэнэ — тест бүрт модулийг ДАХИН
 * ажиллуулдаг (модулийн түвшний төлөв цэвэрхэн эхэлнэ) ч дахин хөрвүүлэхгүй.
 */

import { compileModule } from "@/lib/sandbox/react-runtime/transform";

export type Builtins = Record<string, unknown>;

interface ModuleRecord {
  exports: Record<string, unknown>;
}

const EXTENSIONS = ["", ".jsx", ".js", ".json", ".css", "/index.jsx", "/index.js"];

const compiled = new Map<string, string>();

function dirname(path: string): string {
  const index = path.lastIndexOf("/");
  return index === -1 ? "" : path.slice(0, index);
}

/** `./components/../Card` → `Card` */
function normalize(path: string): string {
  const parts: string[] = [];
  for (const part of path.split("/")) {
    if (part === "" || part === ".") continue;
    if (part === "..") parts.pop();
    else parts.push(part);
  }
  return parts.join("/");
}

export class ModuleNotFoundError extends Error {
  constructor(specifier: string, from: string) {
    super(
      specifier.startsWith(".")
        ? `«${specifier}» файл олдсонгүй (${from} файлаас импортолсон). Файлын нэрээ шалгана уу.`
        : `«${specifier}» сан энэ sandbox-д байхгүй. Боломжтой: react, react-dom, react-router, @tanstack/react-query.`,
    );
    this.name = "ModuleNotFoundError";
  }
}

export class ModuleSystem {
  private cache = new Map<string, ModuleRecord>();

  constructor(
    private files: Map<string, string>,
    private builtins: Builtins,
    private onStyle: (name: string, css: string) => void,
  ) {}

  /** Тест бүрийн өмнө — модулиудыг дахин ажиллуулна. */
  reset(): void {
    this.cache.clear();
  }

  has(name: string): boolean {
    return this.files.has(name);
  }

  resolve(specifier: string, from: string): string {
    if (!specifier.startsWith(".") && !specifier.startsWith("/")) {
      if (specifier in this.builtins) return specifier;
      throw new ModuleNotFoundError(specifier, from);
    }
    const base = specifier.startsWith("/") ? specifier : `${dirname(from)}/${specifier}`;
    const target = normalize(base);
    for (const extension of EXTENSIONS) {
      if (this.files.has(target + extension)) return target + extension;
    }
    throw new ModuleNotFoundError(specifier, from);
  }

  require(specifier: string, from: string): unknown {
    const name = this.resolve(specifier, from);
    if (name in this.builtins && !this.files.has(name)) return this.builtins[name];
    return this.load(name);
  }

  /** Файлыг нэрээр нь ажиллуулж `exports`-ийг буцаана. */
  load(name: string): Record<string, unknown> {
    const cached = this.cache.get(name);
    if (cached) return cached.exports;

    const code = this.files.get(name);
    if (code === undefined) throw new ModuleNotFoundError(`./${name}`, name);

    const record: ModuleRecord = { exports: {} };
    this.cache.set(name, record);

    if (name.endsWith(".css")) {
      this.onStyle(name, code);
      return record.exports;
    }

    const key = `${name}\u0000${code}`;
    let source = compiled.get(key);
    if (source === undefined) {
      source = compileModule(code, name);
      compiled.set(key, source);
    }

    // Шууд бус eval: сурагчийн код runtime-ийн хувьсагчдыг харахгүй. Функцийн
    // толгой нь кодын эхний мөртэй нэг мөрөнд — мөрийн дугаар зөв үлдэнэ.
    // `sourceURL` нь алдааны stack дээр «App.jsx:12:5» гэж харуулна.
    const factory = (0, eval)(
      `(function (require, module, exports) {${source}\n})\n//# sourceURL=${name}`,
    ) as (
      require: (specifier: string) => unknown,
      module: ModuleRecord,
      exports: Record<string, unknown>,
    ) => void;

    try {
      factory((specifier) => this.require(specifier, name), record, record.exports);
    } catch (error) {
      this.cache.delete(name);
      throw error;
    }
    return record.exports;
  }
}
