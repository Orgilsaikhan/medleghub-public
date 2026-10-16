import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import ts from "typescript";

const compiled = mkdtempSync(path.join(tmpdir(), "medleghub-flow-tests-"));
execFileSync(process.execPath, ["node_modules/typescript/bin/tsc", "--target", "ES2022", "--module", "commonjs", "--skipLibCheck", "--outDir", compiled, "src/lib/flowgorithm/model.ts", "src/lib/flowgorithm/expression.ts", "src/lib/flowgorithm/runtime.ts", "src/lib/flowgorithm/layout.ts", "src/lib/flowgorithm/testing.ts"], { stdio: "pipe" });
const require = createRequire(import.meta.url);
const { FlowRuntime } = require(path.join(compiled, "runtime.js"));
const { compileExpression } = require(path.join(compiled, "expression.js"));
const { emptyProgram, editProgram, exportFprg, newNode, parseProgram } = require(path.join(compiled, "model.js"));
const { layoutProgram } = require(path.join(compiled, "layout.js"));
const { executeFlow } = require(path.join(compiled, "testing.js"));
// The same output normalisation the browser grader uses (type-only imports, so a plain transpile is enough).
const graderSource = ts.transpileModule(readFileSync("src/lib/sandbox/grader.ts", "utf8"), { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
const { normalizeOutput } = await import(`data:text/javascript;base64,${Buffer.from(graderSource).toString("base64")}`);
let serial = 0;
const node = (kind, fields = {}) => ({ id: `test-${++serial}`, kind, ...fields });
const output = (expression, newline = true) => node("output", { expression, newline });
const declare = (name, dataType = "Integer") => node("declare", { name, dataType });
const assign = (name, expression) => node("assign", { name, expression });
const program = (nodes) => ({ ...emptyProgram(), nodes });
const evaluate = (expression) => compileExpression(expression)((name) => { throw new Error(`unknown ${name}`); });
function run(nodes, inputs = []) {
  const runtime = new FlowRuntime(program(nodes));
  let result = runtime.iterator.next(); let index = 0;
  while (!result.done) {
    if (result.value.kind === "input") {
      assert.ok(index < inputs.length, "A required input was not supplied");
      result = runtime.iterator.next(String(inputs[index++]));
    } else result = runtime.iterator.next();
  }
  assert.equal(index, inputs.length, "Unexpected unused inputs");
  return runtime.snapshot();
}

for (const [expression, expected] of [
  ["2 + 3 * 4", 14], ["(2 + 3) * 4", 20], ["7 / 2", 3.5], ["-3 mod 2 == 0", false],
  ['"2 + 3"', "2 + 3"], ['"Нийт: " & (2 + 3)', "Нийт: 5"], ["true and not false", true],
  ["false and (1 / 0 == 0)", false], ["true or missing == 1", true], ["2^3*2", 16],
  ["ToInteger(\"12\") + 1", 13], ['Len("Монгол")', 6], ["ToFixed(7 / 2, 2)", "3.50"],
]) test(`expression: ${expression}`, () => assert.equal(evaluate(expression), expected));

for (const expression of ["window.alert(1)", "fetch(1)", "1; 2", "constructor(1)", '"x" + 1', "1 / 0", "5 mod 0", "true + 2", "missing", "1 +", '(1 + 2', '"no end', "Sqrt(-1)", "1e999"]) {
  test(`rejects: ${expression}`, () => assert.throws(() => evaluate(expression)));
}

test("case-insensitive variables, integer conversion, and output without newline", () => {
  const result = run([declare("Count"), assign("count", "7 / 2"), output('"Count: "', false), output("COUNT")]);
  assert.equal(result.output, "Count: 3\n");
  assert.equal(result.variables[0].value, 3);
});
test("input pauses before assignment, invalid input can be retried", () => {
  const runtime = new FlowRuntime(program([declare("n"), node("input", { name: "n" }), output("n")]));
  assert.equal(runtime.iterator.next().value.kind, "step");
  assert.equal(runtime.iterator.next().value.kind, "input");
  assert.throws(() => runtime.validateInput("n", "3.5"));
  assert.throws(() => runtime.validateInput("n", "hello"));
  runtime.validateInput("n", "7");
  runtime.iterator.next("7"); runtime.iterator.next();
  assert.equal(runtime.snapshot().output, "7\n");
});
test("For includes its endpoint, supports descending and non-unit steps", () => {
  const ascending = node("for", { name: "i", start: "2", end: "6", step: "2", direction: "inc", body: [output("i")] });
  assert.equal(run([declare("i"), ascending]).output, "2\n4\n6\n");
  assert.equal(run([declare("i"), { ...ascending, start: "5", end: "1", direction: "dec" }]).output, "5\n3\n1\n");
  assert.throws(() => run([declare("i"), { ...ascending, step: "0" }]), /Step/);
});
test("While may execute zero times; Do executes once before checking", () => {
  assert.equal(run([node("while", { expression: "false", body: [output("1")] })]).output, "");
  assert.equal(run([node("do", { expression: "false", body: [output("1")] })]).output, "1\n");
});
test("nested If executes only the selected branch", () => {
  const inner = node("if", { expression: "true", trueBranch: [output('"yes"')], falseBranch: [output("1 / 0")] });
  assert.equal(run([node("if", { expression: "false", trueBranch: [output("missing")], falseBranch: [inner] })]).output, "yes\n");
});
test("empty infinite loops are bounded", () => {
  assert.throws(() => run([node("while", { expression: "true", body: [] })]), /10 000/);
});
test("output is bounded even when an infinite loop prints", () => {
  assert.throws(() => run([node("while", { expression: "true", body: [output('"12345678901234567890"')] })]), /20 000/);
});
test("undeclared, uninitialized and duplicate variables report errors", () => {
  assert.throws(() => run([assign("a", "1")]), /Declare/);
  assert.throws(() => run([declare("a"), output("a")]), /утга оноогоогүй/);
  assert.throws(() => run([declare("a"), declare("A")]), /өмнө нь/);
  assert.throws(() => run([declare("a", "Boolean"), assign("a", "1")]), /төрөлтэй/);
});
test("breakpoints yield a pause event then continue normally", () => {
  const runtime = new FlowRuntime(program([node("breakpoint"), output("42")]));
  assert.equal(runtime.iterator.next().value.kind, "breakpoint");
  runtime.iterator.next(); assert.equal(runtime.snapshot().output, "42\n");
});
test("editing a nested branch preserves the original program and other branches", () => {
  const conditional = node("if", { expression: "true", trueBranch: [], falseBranch: [output("2")] });
  const original = program([conditional]);
  const next = editProgram(original, { point: { ownerId: conditional.id, branch: "trueBranch", index: 0 }, node: output("1") });
  assert.equal(original.nodes[0].trueBranch.length, 0);
  assert.equal(run(next.nodes).output, "1\n");
  assert.equal(next.nodes[0].falseBranch[0].expression, "2");
  assert.equal(editProgram(next, { id: conditional.id, node: null }).nodes.length, 0);
});
test("draft validation rejects malformed and oversized trees", () => {
  assert.throws(() => parseProgram(JSON.stringify({ version: 9, nodes: [] })));
  assert.throws(() => parseProgram(JSON.stringify(program([node("if", { expression: "true" })]))));
  assert.throws(() => parseProgram(JSON.stringify(program(Array.from({ length: 201 }, () => output("1"))))));
  const duplicate = output("1");
  assert.throws(() => parseProgram(JSON.stringify(program([duplicate, duplicate]))));
});
test("FPRG export escapes text and retains nested branch and loop structures", () => {
  const nodes = [declare("n"), node("if", { expression: "n < 5", trueBranch: [output('"A & B"')], falseBranch: [node("while", { expression: "false", body: [] })] })];
  const xml = exportFprg(program(nodes));
  assert.match(xml, /expression="n &lt; 5"/);
  assert.match(xml, /&quot;A &amp; B&quot;/);
  assert.match(xml, /<then>/); assert.match(xml, /<else><while/);
});

// Load the real curriculum, so every shipped example is exercised by the same runtime as the UI.
const apiDirectory = path.resolve("../api");
const venvPython = path.join(apiDirectory, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
const fixtureSource = execFileSync(existsSync(venvPython) ? venvPython : "python", ["-c", "import json; from app.content.flowgorithm import FLOWGORITHM_COURSE as c; from app.content.exercises import exercise_payload; print(json.dumps({l.slug: {'starter': json.loads(l.initial_code), 'exercise': exercise_payload(l.exercise)} for m in c.modules for l in m.lessons}))"], { cwd: apiDirectory, encoding: "utf8" });
const fixtures = JSON.parse(fixtureSource);
const cases = {
  "input-mendchilgee": [["Сараа"], "Сайн уу, Сараа!\n"],
  "niilber-dundaj": [[4, 7], "Нийлбэр: 11\nДундаж: 5.5\n"],
  "if-hoyor-zam": [[60], "Тэнцлээ\nШалгалт дууслаа\n"],
  "davhar-if": [[0], "Тэг\n"], "logik-zuv-orolt": [[101], "0–100 хооронд оруулна уу\n"],
  "ih-toog-oloh": [[-2, -7], "-2\n"], "tegsh-sondgoi": [[-3], "Сондгой\n"],
  "niilber-tsugluulah": [[4], "10\n"], "orolt-dahin-asuu": [[-5, 101, 80], "Хүлээн авсан оноо: 80\n"],
  "tusul-delguur": [[2000, 3, 5000], "Нийт үнэ: 6000\nДутах мөнгө: 1000\n"],
  "tusul-dundaj-soril": [[-1, 80, 101, 90, 100], "Дундаж: 90\nТэнцлээ\n"],
  "anhnii-output": [[2, 3], "Сайн уу, дэлхий!\n5\na + b\n"],
  "suulgah-ehleh": [[12], "Сайн уу!\n12\n"], "durs-sum": [[3], "3\nХөөрлөө!\n"],
  "while-davtalt": [[], "1\n2\n3\n4\n5\nДууслаа\n"], "for-tooluur": [[], "1\n2\n3\n4\n5\n"],
  "utga-onooh": [[10], "10\n15\n"], "alhamaar-shalgah": [[], "10\n16\n"],
  "hartsuulalt-boolean": [[], "true\n"], "operator-uldegdel": [[], "14\n20\n0\n1\n"],
  "program-gej-yu-ve": [[3000, 2500], "3500\n"], "algoritm-alham": [[8, 12], "14\n"],
  "orolt-garalt": [[5, 3], "15\n"],
};
// This starter is the task itself: the student adds the missing Declare shapes.
const starterErrors = { "huvisagch-turul": /Declare/ };
assert.equal(Object.keys(fixtures).length, 24);
for (const [slug, { starter }] of Object.entries(fixtures)) test(`curriculum runs and lays out: ${slug}`, () => {
  const parsed = parseProgram(JSON.stringify(starter));
  const [inputs, ending] = cases[slug] ?? [[], undefined];
  if (starterErrors[slug]) assert.throws(() => run(parsed.nodes, inputs), starterErrors[slug]);
  else {
    const result = run(parsed.nodes, inputs);
    if (ending !== undefined) assert.ok(result.output.endsWith(ending), result.output);
  }
  const layout = layoutProgram(parsed);
  assert.ok(Number.isFinite(layout.width) && Number.isFinite(layout.height));
  for (const shape of layout.shapes) {
    assert.ok(shape.x - shape.width / 2 >= 0 && shape.x + shape.width / 2 <= layout.width);
    assert.ok(shape.y >= 0 && shape.y + shape.height <= layout.endY);
  }
});

// Every lesson's task: the reference solution passes each test and the starter fails at least one,
// graded exactly like the lesson page (executeFlow + normalizeOutput).
const passes = (program, testCase) => {
  const result = executeFlow(program, testCase.stdin);
  return !result.error && normalizeOutput(result.answer) === normalizeOutput(testCase.expected_output);
};
test("every lesson has a graded task", () => {
  assert.equal(Object.values(fixtures).filter(({ exercise }) => exercise?.tests.length).length, 24);
});
for (const [slug, { starter, exercise }] of Object.entries(fixtures)) {
  if (!exercise) continue;
  test(`task: solution passes, starter fails: ${slug}`, () => {
    const solution = parseProgram(exercise.solution);
    for (const [index, testCase] of exercise.tests.entries()) {
      const result = executeFlow(solution, testCase.stdin);
      assert.equal(result.error, undefined, `test ${index + 1}: ${result.error}`);
      assert.equal(normalizeOutput(result.answer), normalizeOutput(testCase.expected_output), `test ${index + 1}`);
    }
    const program = parseProgram(JSON.stringify(starter));
    assert.ok(exercise.tests.some((testCase) => !passes(program, testCase)), "the starter already passes every test");
    assert.ok(Number.isFinite(layoutProgram(solution).height));
  });
}

test("graded output starts after the last Input, so prompts and retry messages are ignored", () => {
  const read = () => node("input", { name: "n" });
  const nodes = [output('"Welcome"'), declare("n"), output('"Number:"'), read(), output('"Again:"'), read(), output("n * 2"), output('"done"')];
  const result = executeFlow(program(nodes), "1\n21\n");
  assert.equal(result.error, undefined);
  assert.equal(result.answer, "42\ndone\n");
  assert.equal(executeFlow(program([output('"no input: all output counts"')]), "").answer, "no input: all output counts\n");
});
test("tests report running out of input and inputs that do not fit the variable type", () => {
  const read = () => node("input", { name: "n" });
  assert.match(executeFlow(program([declare("n"), read(), read()]), "5\n").error, /оролт дууссан/);
  assert.match(executeFlow(program([declare("n"), read()]), "4.5\n").error, /n \(Integer\)/);
  assert.match(executeFlow(program([node("while", { expression: "true", body: [] })]), "").error, /10 000/);
  assert.equal(executeFlow(program([declare("s", "String"), node("input", { name: "s" }), output("s")]), "Сараа\r\n").answer, "Сараа\n");
});

test("new shapes get unique ids without crypto.randomUUID (plain-HTTP LAN dev server)", () => {
  // Browsers expose randomUUID only in secure contexts; http://192.168.x.x has none.
  const original = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(crypto), "randomUUID");
  Object.defineProperty(Object.getPrototypeOf(crypto), "randomUUID", { value: undefined, configurable: true });
  try {
    const ids = new Set(Array.from({ length: 200 }, () => newNode("declare").id));
    assert.equal(ids.size, 200);
    for (const id of ids) assert.match(id, /^[0-9a-f]{32}$/);
  } finally {
    Object.defineProperty(Object.getPrototypeOf(crypto), "randomUUID", original);
  }
  assert.equal(typeof crypto.randomUUID, "function");
});
