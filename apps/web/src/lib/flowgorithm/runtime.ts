import { compileExpression, logical, numeric, RESERVED, type Value } from "./expression";
import {
  declaredNames,
  isIncomplete,
  LABELS,
  parseProgram,
  type DataType,
  type FlowNode,
  type FlowProgram,
} from "./model";

export interface Variable {
  name: string;
  type: DataType;
  value: Value | null;
}
export interface RuntimeEvent {
  kind: "step" | "input" | "breakpoint";
  nodeId: string;
  variable?: Variable;
}
export interface RuntimeSnapshot {
  variables: Variable[];
  output: string;
  steps: number;
}

export class FlowRuntime {
  readonly iterator: Generator<RuntimeEvent, void, string | undefined>;
  private variables = new Map<string, Variable>();
  private expressions = new Map<string, ReturnType<typeof compileExpression>>();
  private output = "";
  /** Сүүлчийн Input-ийн дараах гаралт хаанаас эхлэхийг заана — `answer()`. */
  private answerFrom = 0;
  private steps = 0;
  activeId: string | null = null;

  constructor(program: FlowProgram) {
    parseProgram(JSON.stringify(program));
    this.iterator = this.execute(program.nodes);
  }

  snapshot(): RuntimeSnapshot {
    return {
      variables: [...this.variables.values()].map((v) => ({ ...v })),
      output: this.output,
      steps: this.steps,
    };
  }

  /**
   * Даалгаврын шалгагчийн харьцуулах гаралт: сүүлчийн Input-ээс хойш гарсан
   * бүх зүйл. Input-ийн өмнөх асуулт («Нэрээ оруулна уу:»), «дахин оруул»
   * гэх мэт мэдэгдэл тооцогдохгүй — Python-ы тестийн `quiet_input`-тэй адил.
   */
  answer(): string {
    return this.output.slice(this.answerFrom);
  }

  private tick(node: FlowNode): RuntimeEvent {
    this.activeId = node.id;
    if (++this.steps > 10_000)
      throw new Error("10 000 алхмын хязгаарт хүрлээ. Давталтын зогсох нөхцөлийг шалгаарай.");
    return { kind: "step", nodeId: node.id };
  }

  private variable(name = ""): Variable {
    if (declaredNames(name).length > 1)
      throw new Error(
        `«${name}»: энэ дүрсэнд нэг л хувьсагч бичнэ. Хувьсагч бүрт тусдаа дүрс нэмнэ үү.`,
      );
    const variable = this.variables.get(name.trim().toLowerCase());
    if (!variable) throw new Error(`«${name}» хувьсагчийг эхлээд Declare-ээр зарлана уу.`);
    return variable;
  }

  private evaluate(source = ""): Value {
    let expression = this.expressions.get(source);
    if (!expression) {
      expression = compileExpression(source);
      this.expressions.set(source, expression);
    }
    return expression((name) => {
      const variable = this.variable(name);
      if (variable.value === null)
        throw new Error(`«${variable.name}» хувьсагчид утга оноогоогүй байна.`);
      return variable.value;
    });
  }

  private assign(name: string | undefined, value: Value) {
    const variable = this.variable(name);
    if (variable.type === "Integer" || variable.type === "Real") {
      const number = numeric(value);
      variable.value = variable.type === "Integer" ? Math.trunc(number) : number;
      if (variable.type === "Integer" && !Number.isSafeInteger(variable.value))
        throw new Error("Бүхэл тоо зөвшөөрөх хэмжээнээс хэтэрлээ.");
    } else {
      const expected = variable.type === "String" ? "string" : "boolean";
      if (typeof value !== expected)
        throw new Error(
          `«${variable.name}» нь ${variable.type} төрөлтэй. Утгын төрлөө шалгана уу.`,
        );
      variable.value = value;
    }
  }

  validateInput(name: string, text: string): Value {
    const variable = this.variable(name);
    if (text.length > 1000) throw new Error("Оролт 1000 тэмдэгтээс урт байна.");
    if (variable.type === "String") return text;
    const value = text.trim();
    if (variable.type === "Boolean") {
      if (!/^(true|false)$/i.test(value)) throw new Error("true эсвэл false гэж оруулна уу.");
      return value.toLowerCase() === "true";
    }
    const pattern =
      variable.type === "Integer" ? /^[+-]?\d+$/ : /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/i;
    if (!pattern.test(value) || !Number.isFinite(Number(value)))
      throw new Error(`${variable.type === "Integer" ? "Бүхэл" : "Бодит"} тоо оруулна уу.`);
    if (variable.type === "Integer" && !Number.isSafeInteger(Number(value)))
      throw new Error("Бүхэл тоо хэт их байна.");
    return Number(value);
  }

  private *execute(nodes: FlowNode[]): Generator<RuntimeEvent, void, string | undefined> {
    for (const node of nodes) {
      this.activeId = node.id;
      if (isIncomplete(node))
        throw new Error(
          `«${LABELS[node.kind]}» дүрсийн утгыг оруулаагүй байна. Дүрсэн дээр дарж бөглөнө үү.`,
        );
      switch (node.kind) {
        case "declare": {
          for (const name of declaredNames(node.name)) {
            const key = name.toLowerCase();
            if (!/^[a-z][a-z0-9]*$/i.test(name) || RESERVED.has(key))
              throw new Error(
                `«${name}» нэр тохирохгүй. Латин үсгээр эхэлсэн, зайгүй нэр өгнө үү.`,
              );
            if (this.variables.has(key))
              throw new Error(`«${name}» хувьсагч өмнө нь зарлагдсан байна.`);
            if (this.variables.size >= 200) throw new Error("Хувьсагчийн тоо хэтэрлээ.");
            this.variables.set(key, { name, type: node.dataType!, value: null });
          }
          yield this.tick(node);
          break;
        }
        case "assign":
          this.assign(node.name, this.evaluate(node.expression));
          yield this.tick(node);
          break;
        case "output": {
          const text = String(this.evaluate(node.expression)) + (node.newline ? "\n" : "");
          if (this.output.length + text.length > 20_000)
            throw new Error("Гаралтын 20 000 тэмдэгтийн хязгаарт хүрлээ.");
          this.output += text;
          yield this.tick(node);
          break;
        }
        case "input": {
          const variable = this.variable(node.name);
          const input = yield { kind: "input", nodeId: node.id, variable: { ...variable } };
          this.assign(node.name, this.validateInput(variable.name, input ?? ""));
          this.answerFrom = this.output.length;
          yield this.tick(node);
          break;
        }
        case "if": {
          const condition = logical(this.evaluate(node.expression));
          yield this.tick(node);
          yield* this.execute(condition ? node.trueBranch! : node.falseBranch!);
          break;
        }
        case "while": {
          while (true) {
            const condition = logical(this.evaluate(node.expression));
            yield this.tick(node);
            if (!condition) break;
            yield* this.execute(node.body!);
          }
          break;
        }
        case "do": {
          while (true) {
            yield* this.execute(node.body!);
            const condition = logical(this.evaluate(node.expression));
            yield this.tick(node);
            if (!condition) break;
          }
          break;
        }
        case "for": {
          if (this.variable(node.name).type !== "Integer")
            throw new Error("For-ийн тоолуурыг Integer гэж зарлана уу.");
          const start = numeric(this.evaluate(node.start));
          const end = numeric(this.evaluate(node.end));
          const step = numeric(this.evaluate(node.step));
          if (![start, end, step].every(Number.isSafeInteger) || step <= 0)
            throw new Error("For-ийн эхлэл, төгсгөл бүхэл тоо; Step нь эерэг бүхэл тоо байна.");
          this.assign(node.name, start);
          while (true) {
            const value = numeric(this.variable(node.name).value!);
            const condition = node.direction === "inc" ? value <= end : value >= end;
            yield this.tick(node);
            if (!condition) break;
            yield* this.execute(node.body!);
            this.assign(
              node.name,
              numeric(this.variable(node.name).value!) + (node.direction === "inc" ? step : -step),
            );
          }
          break;
        }
        case "comment":
          yield this.tick(node);
          break;
        case "breakpoint":
          yield { ...this.tick(node), kind: "breakpoint" };
          break;
      }
    }
  }
}
