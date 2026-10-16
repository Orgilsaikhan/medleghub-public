/** Small, closed expression language. Never passes learner text to eval/Function. */
export type Value = string | number | boolean;
type Token = { kind: "value"; value: Value } | { kind: "name" | "op"; value: string };
type Expr =
  | { kind: "value"; value: Value }
  | { kind: "name"; name: string }
  | { kind: "unary"; op: string; arg: Expr }
  | { kind: "binary"; op: string; left: Expr; right: Expr }
  | { kind: "call"; name: string; args: Expr[] };

const precedence: Record<string, number> = {
  or: 1,
  "||": 1,
  and: 2,
  "&&": 2,
  "==": 3,
  "=": 3,
  "!=": 3,
  "<>": 3,
  "<": 3,
  ">": 3,
  "<=": 3,
  ">=": 3,
  "&": 4,
  "+": 5,
  "-": 5,
  "*": 6,
  "/": 6,
  "%": 6,
  mod: 6,
  "^": 7,
};
export const RESERVED = new Set([
  "true",
  "false",
  "and",
  "or",
  "not",
  "mod",
  "pi",
  "integer",
  "real",
  "string",
  "boolean",
  "abs",
  "sqrt",
  "len",
  "int",
  "tointeger",
  "toreal",
  "tostring",
  "tofixed",
]);

export function numeric(value: Value): number {
  if (typeof value !== "number" || !Number.isFinite(value))
    throw new Error("Энэ үйлдэлд тоон утга хэрэгтэй.");
  return value;
}
export function logical(value: Value): boolean {
  if (typeof value !== "boolean") throw new Error("Нөхцөл нь true эсвэл false байх ёстой.");
  return value;
}
function bounded(value: Value): Value {
  if (typeof value === "number" && !Number.isFinite(value))
    throw new Error("Тооцооны хариу хэт их эсвэл тодорхойгүй байна.");
  if (typeof value === "string" && value.length > 10_000) throw new Error("Текст хэт урт боллоо.");
  return value;
}

function tokenize(source: string): Token[] {
  if (!source.trim()) throw new Error("Илэрхийлэл хоосон байна.");
  if (source.length > 500) throw new Error("Илэрхийлэл 500 тэмдэгтээс урт байна.");
  const tokens: Token[] = [];
  let i = 0;
  while (i < source.length) {
    const rest = source.slice(i);
    const spaces = /^\s+/.exec(rest);
    if (spaces) {
      i += spaces[0].length;
      continue;
    }
    if (rest[0] === '"') {
      let text = "";
      let closed = false;
      i++;
      while (i < source.length) {
        const char = source[i++];
        if (char === '"') {
          closed = true;
          break;
        }
        if (char === "\\") {
          const escaped = source[i++];
          if (!['"', "\\", "n", "t"].includes(escaped))
            throw new Error("Текстийн escape тэмдэг буруу байна.");
          text += escaped === "n" ? "\n" : escaped === "t" ? "\t" : escaped;
        } else text += char;
      }
      if (!closed) throw new Error('Текстийн хаах хашилт (") дутуу байна.');
      tokens.push({ kind: "value", value: text });
      continue;
    }
    const number = /^(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?/i.exec(rest);
    if (number) {
      tokens.push({ kind: "value", value: numeric(Number(number[0])) });
      i += number[0].length;
      continue;
    }
    const name = /^[a-z][a-z0-9]*/i.exec(rest);
    if (name) {
      const word = name[0].toLowerCase();
      i += name[0].length;
      if (word === "true" || word === "false")
        tokens.push({ kind: "value", value: word === "true" });
      else if (["and", "or", "not", "mod"].includes(word)) tokens.push({ kind: "op", value: word });
      else tokens.push({ kind: "name", value: word });
      continue;
    }
    const op = /^(?:==|!=|<=|>=|<>|&&|\|\||[+\-*/%^&=<>!(),])/.exec(rest);
    if (!op) throw new Error(`Танихгүй тэмдэг: ${rest[0]}.`);
    tokens.push({ kind: "op", value: op[0] });
    i += op[0].length;
  }
  if (tokens.length > 160) throw new Error("Илэрхийлэл хэт олон үйлдэлтэй байна.");
  return tokens;
}

export function compileExpression(source: string): (lookup: (name: string) => Value) => Value {
  const tokens = tokenize(source);
  let position = 0;
  const at = (op: string) => tokens[position]?.kind === "op" && tokens[position]?.value === op;
  const expect = (op: string) => {
    if (!at(op)) throw new Error(`«${op}» тэмдэг дутуу байна.`);
    position++;
  };
  const parse = (minimum = 1): Expr => {
    const token = tokens[position++];
    if (!token) throw new Error("Илэрхийллийн утга дутуу байна.");
    let left: Expr;
    if (token.kind === "value") left = token;
    else if (token.kind === "name") {
      if (at("(")) {
        position++;
        const args: Expr[] = [];
        if (!at(")")) {
          args.push(parse());
          while (at(",")) {
            position++;
            args.push(parse());
          }
        }
        expect(")");
        left = { kind: "call", name: token.value, args };
      } else left = { kind: "name", name: token.value };
    } else if (token.value === "(") {
      left = parse();
      expect(")");
    } else if (["-", "+", "!", "not"].includes(token.value))
      left = { kind: "unary", op: token.value, arg: parse(8) };
    else throw new Error(`«${token.value}» тэмдгийн өмнө утга хэрэгтэй.`);
    while (tokens[position]?.kind === "op") {
      const op = String(tokens[position].value);
      const level = precedence[op];
      if (!level || level < minimum) break;
      position++;
      left = { kind: "binary", op, left, right: parse(level + 1) };
    }
    return left;
  };
  const ast = parse();
  if (position !== tokens.length) throw new Error("Илэрхийлэлд илүү тэмдэг эсвэл утга байна.");

  return (lookup) => {
    const evaluate = (expr: Expr): Value => {
      if (expr.kind === "value") return expr.value;
      if (expr.kind === "name") return expr.name === "pi" ? Math.PI : lookup(expr.name);
      if (expr.kind === "unary") {
        const value = evaluate(expr.arg);
        return expr.op === "!" || expr.op === "not"
          ? !logical(value)
          : expr.op === "-"
            ? -numeric(value)
            : numeric(value);
      }
      if (expr.kind === "call") {
        const args = expr.args.map(evaluate);
        if (args.length !== (expr.name === "tofixed" ? 2 : 1))
          throw new Error("Функцийн аргументын тоо буруу байна.");
        const value = args[0];
        switch (expr.name) {
          case "abs":
            return Math.abs(numeric(value));
          case "sqrt":
            return bounded(Math.sqrt(numeric(value)));
          case "int":
            return Math.trunc(numeric(value));
          case "len":
            if (typeof value !== "string") throw new Error("Len-д текст өгнө.");
            return value.length;
          case "tostring":
            return String(value);
          case "toreal":
          case "tointeger": {
            if (
              typeof value !== "string" ||
              !/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/i.test(value.trim())
            )
              throw new Error("Текстийг тоо болгох боломжгүй байна.");
            const number = numeric(Number(value));
            return expr.name === "tointeger" ? Math.trunc(number) : number;
          }
          case "tofixed": {
            const digits = numeric(args[1]);
            if (!Number.isInteger(digits) || digits < 0 || digits > 10)
              throw new Error("Оронгийн тоо 0–10 хооронд байна.");
            return numeric(value).toFixed(digits);
          }
          default:
            throw new Error(`«${expr.name}» функцийг энэ засварлагч дэмжихгүй.`);
        }
      }
      const a = evaluate(expr.left);
      if (expr.op === "and" || expr.op === "&&") return logical(a) && logical(evaluate(expr.right));
      if (expr.op === "or" || expr.op === "||") return logical(a) || logical(evaluate(expr.right));
      const b = evaluate(expr.right);
      switch (expr.op) {
        case "&":
          return bounded(String(a) + String(b));
        case "+":
          return bounded(numeric(a) + numeric(b));
        case "-":
          return bounded(numeric(a) - numeric(b));
        case "*":
          return bounded(numeric(a) * numeric(b));
        case "^":
          return bounded(numeric(a) ** numeric(b));
        case "/":
        case "%":
        case "mod":
          if (numeric(b) === 0) throw new Error("Тэгээр хувааж болохгүй.");
          return bounded(expr.op === "/" ? numeric(a) / numeric(b) : numeric(a) % numeric(b));
        default: {
          if (typeof a !== typeof b) throw new Error("Ижил төрлийн утгуудыг харьцуулна уу.");
          if (expr.op === "=" || expr.op === "==") return a === b;
          if (expr.op === "!=" || expr.op === "<>") return a !== b;
          if (expr.op === ">") return a > b;
          if (expr.op === "<") return a < b;
          if (expr.op === ">=") return a >= b;
          return a <= b;
        }
      }
    };
    return bounded(evaluate(ast));
  };
}
