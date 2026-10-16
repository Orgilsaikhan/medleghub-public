/**
 * React sandbox-ийн цэвэр функцууд: олон файлын хэлбэр, ```quiz задлагч,
 * давталтын хамгаалалт, синтакс алдааны мессеж, `srcdoc` дахь JSON.
 *
 *   node --test tests/react-sandbox.test.mjs
 *
 * Хөтөч дээрх бүрэн шалгалтыг `npm run verify:react` хийнэ.
 */

import assert from "node:assert/strict";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { build } from "esbuild";

const root = fileURLToPath(new URL("..", import.meta.url));
const bundle = await build({
  stdin: {
    contents: `
      export * from "@/lib/sandbox/react/files";
      export { parseQuiz } from "@/lib/quiz";
      export { checkSyntax, compileModule, CompileError, guardLoops, LOOP_GUARD } from "@/lib/sandbox/react-runtime/transform";
      export { buildDocument, createJob } from "@/lib/sandbox/react/runner";
    `,
    resolveDir: root,
    loader: "ts",
  },
  absWorkingDir: root,
  bundle: true,
  format: "esm",
  platform: "node",
  write: false,
  logLevel: "error",
});
const lib = await import(
  `data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString("base64")}`
);

test("файлуудыг `// @file` мөрөөр хуваана", () => {
  const files = lib.parseLessonFiles(
    [
      "// @file App.jsx",
      "export default function App() {}",
      "",
      "// @file main.jsx locked",
      'import App from "./App";',
      "// @file index.html locked",
      '<div id="root"></div>',
    ].join("\n"),
  );
  assert.deepEqual(
    files.map(({ name, locked }) => [name, locked]),
    [
      ["App.jsx", false],
      ["main.jsx", true],
      ["index.html", true],
    ],
  );
  assert.equal(files[0].code, "export default function App() {}\n");
  assert.equal(lib.entryFile(files), "main.jsx");
  assert.equal(lib.htmlOf(files), '<div id="root"></div>\n');
});

test("тэмдэггүй код нь ганц App.jsx", () => {
  const files = lib.parseLessonFiles("export default function App() {}\n");
  assert.equal(files.length, 1);
  assert.equal(files[0].name, "App.jsx");
  assert.equal(lib.entryFile(files), "App.jsx");
  assert.equal(lib.htmlOf(files), '<div id="root"></div>');
});

test("шийдэл нь ижил нэртэй файлыг орлож, шинийг нэмнэ", () => {
  const base = lib.parseLessonFiles("// @file App.jsx\nold\n// @file main.jsx locked\nmain\n");
  const merged = lib.overlayFiles(
    base,
    lib.parseLessonFiles("// @file App.jsx\nnew\n// @file Card.jsx\ncard\n"),
  );
  assert.deepEqual(
    merged.map((file) => [file.name, file.code.trim(), file.locked]),
    [
      ["App.jsx", "new", false],
      ["main.jsx", "main", true],
      ["Card.jsx", "card", false],
    ],
  );
});

test("```quiz — нэг ба олон зөв хариулт, буруу хэлбэр", () => {
  const single = lib.parseQuiz("`count` хэд вэ?\n- [ ] 2\n- [x] 1\n> Snapshot.\n");
  assert.equal(single.question, "`count` хэд вэ?");
  assert.deepEqual(
    single.options.map((option) => option.correct),
    [false, true],
  );
  assert.equal(single.explanation, "Snapshot.");

  const multiple = lib.parseQuiz("Аль нь hook вэ?\n- [x] useState\n- [x] useEffect\n- [ ] map\n");
  assert.equal(multiple.options.filter((option) => option.correct).length, 2);

  assert.equal(lib.parseQuiz("Зөв хариултгүй\n- [ ] a\n- [ ] b\n"), null);
  assert.equal(lib.parseQuiz("Ганц сонголт\n- [x] a\n"), null);
});

test("давталт бүрт хамгаалалт нэмэгдэнэ — бие нь блокгүй ч", () => {
  const code = [
    "let total = 0;",
    "for (let i = 0; i < 3; i++) total += i;",
    "while (total < 10) { total++; }",
    "do total--; while (total > 8);",
    "for (const x of [1, 2]) total += x;",
    "total;",
  ].join("\n");
  const guarded = lib.guardLoops(code);
  assert.equal(guarded.split(`${lib.LOOP_GUARD}();`).length - 1, 4);
  assert.equal(guarded.split("\n").length, code.split("\n").length, "мөрийн дугаар өөрчлөгдөхгүй");

  let calls = 0;
  const result = new Function(lib.LOOP_GUARD, `${guarded.replace(/total;$/, "return total;")}`)(
    () => {
      calls += 1;
    },
  );
  assert.equal(result, 11);
  assert.ok(calls >= 4);
});

test("синтакс алдаа нь файл, мөр, монгол тайлбартай", () => {
  assert.throws(
    () =>
      lib.compileModule(
        "export default function App() {\n  return <div>hi</span>;\n}\n",
        "App.jsx",
      ),
    (error) => {
      assert.ok(error instanceof lib.CompileError);
      assert.equal(error.detail.file, "App.jsx");
      assert.equal(error.detail.line, 2);
      assert.match(error.detail.message, /<div> шошгыг зөв хаагаагүй/);
      assert.match(error.detail.message, /Expected corresponding JSX closing tag/);
      return true;
    },
  );
  assert.throws(
    () => lib.checkSyntax("function A() { return <h1>a</h1><p>b</p> }", "App.jsx"),
    /нэг л эх элемент/,
  );
});

test("JSX болон import нь CommonJS болж хөрвөнө", () => {
  const output = lib.compileModule(
    'import { useState } from "react";\nexport default function App() { return <p>{1}</p>; }\n',
    "App.jsx",
  );
  assert.match(output, /require\(['"]react['"]\)/);
  assert.match(output, /exports\.default/);
  assert.doesNotMatch(output, /<p>/);
});

test("srcdoc доторх сурагчийн код `</script>`-ээр гарч чадахгүй", () => {
  const files = lib.parseLessonFiles(
    '// @file App.jsx\nconst s = "</script><script>alert(1)</script>";\n',
  );
  const job = lib.createJob(files, "preview");
  const html = lib.buildDocument(job);
  // Жинхэнэ хаалтын шошго: JSON, runtime, boot — гурав.
  assert.equal(html.split("</script>").length - 1, 3);
  assert.match(html, /\\u003c\/script>/);
});
