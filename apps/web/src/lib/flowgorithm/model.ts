export const KINDS = [
  "declare",
  "assign",
  "input",
  "output",
  "if",
  "while",
  "for",
  "do",
  "comment",
  "breakpoint",
] as const;
export type NodeKind = (typeof KINDS)[number];
export type DataType = "Integer" | "Real" | "String" | "Boolean";
export type Branch = "nodes" | "trueBranch" | "falseBranch" | "body";

export interface FlowNode {
  id: string;
  kind: NodeKind;
  name?: string;
  expression?: string;
  dataType?: DataType;
  newline?: boolean;
  start?: string;
  end?: string;
  step?: string;
  direction?: "inc" | "dec";
  trueBranch?: FlowNode[];
  falseBranch?: FlowNode[];
  body?: FlowNode[];
}

export interface FlowProgram {
  format: "medleghub-flowgorithm";
  version: 1;
  nodes: FlowNode[];
}

export interface InsertPoint {
  ownerId: string | null;
  branch: Branch;
  index: number;
}

export const LABELS: Record<NodeKind, string> = {
  declare: "Declare",
  assign: "Assign",
  input: "Input",
  output: "Output",
  if: "If",
  while: "While",
  for: "For",
  do: "Do",
  comment: "Comment",
  breakpoint: "Breakpoint",
};

export const HINTS: Record<NodeKind, string> = {
  declare: "Хувьсагч зарлах",
  assign: "Утга оноох",
  input: "Оролт авах",
  output: "Гаралт харуулах",
  if: "Нөхцөл шалгах",
  while: "Нөхцөлөөр давтах",
  for: "Тоолж давтах",
  do: "Эхлээд хийгээд шалгах",
  comment: "Тайлбар бичих",
  breakpoint: "Энд түр зогсох",
};

export const emptyProgram = (): FlowProgram => ({
  format: "medleghub-flowgorithm",
  version: 1,
  nodes: [],
});

/**
 * Unique shape id.
 *
 * `crypto.randomUUID()` exists only in secure contexts (HTTPS, localhost). Opening
 * the dev server by its network IP (http://192.168.x.x:3000) made every insert fail
 * with "crypto.randomUUID is not a function". `getRandomValues` works everywhere.
 */
function nodeId(): string {
  if (typeof crypto.randomUUID === "function") return crypto.randomUUID();
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

/** Like Flowgorithm, a shape is inserted blank; the student fills it in afterwards. */
export function newNode(kind: NodeKind): FlowNode {
  const node: FlowNode = { id: nodeId(), kind };
  if (kind === "declare") Object.assign(node, { name: "", dataType: "Integer" });
  if (kind === "assign") Object.assign(node, { name: "", expression: "" });
  if (kind === "input") node.name = "";
  if (kind === "output") Object.assign(node, { expression: "", newline: true });
  if (kind === "comment") node.expression = "";
  if (kind === "if") Object.assign(node, { expression: "", trueBranch: [], falseBranch: [] });
  if (kind === "while" || kind === "do") Object.assign(node, { expression: "", body: [] });
  if (kind === "for")
    Object.assign(node, { name: "", start: "", end: "", step: "1", direction: "inc", body: [] });
  return node;
}

const REQUIRED: Partial<Record<NodeKind, (keyof FlowNode)[]>> = {
  declare: ["name"],
  assign: ["name", "expression"],
  input: ["name"],
  output: ["expression"],
  if: ["expression"],
  while: ["expression"],
  do: ["expression"],
  for: ["name", "start", "end", "step"],
};

/** Declare takes several names ("a, b, total"); stray spaces or commas are tolerated. */
export function declaredNames(name = ""): string[] {
  return name.split(/[\s,;]+/).filter(Boolean);
}

/** True while a shape still has a blank field it needs before it can run. */
export function isIncomplete(node: FlowNode): boolean {
  return (REQUIRED[node.kind] ?? []).some((key) => !String(node[key] ?? "").trim());
}

/** Validate persisted/received data before rendering or executing it. */
export function parseProgram(source: string): FlowProgram {
  if (source.length > 200_000) throw new Error("Схемийн файл хэт том байна.");
  const value = JSON.parse(source) as FlowProgram;
  if (!value || value.format !== "medleghub-flowgorithm" || value.version !== 1)
    throw new Error("Схемийн формат танигдсангүй.");
  const ids = new Set<string>();
  function visit(nodes: FlowNode[], depth: number) {
    if (!Array.isArray(nodes) || depth > 10)
      throw new Error("Схемийн бүтэц буруу эсвэл хэт олон давхар байна.");
    for (const node of nodes) {
      if (
        !node ||
        !KINDS.includes(node.kind) ||
        typeof node.id !== "string" ||
        !node.id ||
        ids.has(node.id)
      )
        throw new Error("Дүрсний мэдээлэл буруу байна.");
      ids.add(node.id);
      if (ids.size > 200) throw new Error("Нэг схемд хамгийн ихдээ 200 дүрс нэмнэ.");
      const requireText = (key: keyof FlowNode) => {
        if (typeof node[key] !== "string" || (node[key] as string).length > 500)
          throw new Error("Дүрсний талбар буруу байна.");
      };
      if (["declare", "assign", "input", "for"].includes(node.kind)) requireText("name");
      if (["assign", "output", "if", "while", "do", "comment"].includes(node.kind))
        requireText("expression");
      if (
        node.kind === "declare" &&
        !["Integer", "Real", "String", "Boolean"].includes(node.dataType ?? "")
      )
        throw new Error("Хувьсагчийн төрөл буруу байна.");
      if (node.kind === "output" && typeof node.newline !== "boolean")
        throw new Error("New Line сонголт буруу байна.");
      if (node.kind === "for") {
        for (const key of ["start", "end", "step"] as const) requireText(key);
        if (node.direction !== "inc" && node.direction !== "dec")
          throw new Error("Давталтын чиглэл буруу байна.");
      }
      if (node.kind === "if") {
        visit(node.trueBranch!, depth + 1);
        visit(node.falseBranch!, depth + 1);
      }
      if (["while", "for", "do"].includes(node.kind)) visit(node.body!, depth + 1);
    }
  }
  visit(value.nodes, 0);
  return value;
}

export function children(node: FlowNode): FlowNode[][] {
  return node.kind === "if"
    ? [node.trueBranch ?? [], node.falseBranch ?? []]
    : node.body
      ? [node.body]
      : [];
}

export function findNode(nodes: FlowNode[], id: string): FlowNode | undefined {
  for (const node of nodes) {
    if (node.id === id) return node;
    for (const branch of children(node)) {
      const found = findNode(branch, id);
      if (found) return found;
    }
  }
}

export function editProgram(
  program: FlowProgram,
  change: { point: InsertPoint; node: FlowNode } | { id: string; node: FlowNode | null },
): FlowProgram {
  const next = structuredClone(program);
  if ("point" in change) {
    const { ownerId, branch, index } = change.point;
    const target = ownerId
      ? findNode(next.nodes, ownerId)?.[branch as "body" | "trueBranch" | "falseBranch"]
      : next.nodes;
    if (!target) throw new Error("Дүрс нэмэх байрлал олдсонгүй.");
    target.splice(index, 0, change.node);
  } else {
    const visit = (nodes: FlowNode[]): boolean => {
      const index = nodes.findIndex((node) => node.id === change.id);
      if (index >= 0) {
        nodes.splice(index, 1, ...(change.node ? [change.node] : []));
        return true;
      }
      return nodes.some((node) => children(node).some(visit));
    };
    visit(next.nodes);
  }
  return parseProgram(JSON.stringify(next));
}

export function nodeText(node: FlowNode): string {
  if (isIncomplete(node)) return LABELS[node.kind];
  switch (node.kind) {
    case "declare":
      return `${node.dataType} ${node.name}`;
    case "assign":
      return `${node.name} = ${node.expression}`;
    case "input":
      return `Input ${node.name}`;
    case "for":
      return `${node.name} = ${node.start} … ${node.end} (${node.direction === "dec" ? "−" : "+"}${node.step})`;
    case "breakpoint":
      return "Breakpoint";
    default:
      return node.expression || LABELS[node.kind];
  }
}

function xml(value: string): string {
  return value.replace(
    /[<>&"']/g,
    (char) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;", "'": "&apos;" })[char]!,
  );
}

/** Flowgorithm's native XML format; no executable JavaScript is generated. */
export function exportFprg(program: FlowProgram): string {
  const block = (nodes: FlowNode[]): string =>
    nodes
      .map((node) => {
        const exp = xml(node.expression ?? "");
        const name = xml(node.name ?? "");
        switch (node.kind) {
          case "declare":
            return `<declare name="${xml(declaredNames(node.name).join(", "))}" type="${node.dataType}" array="False" size=""/>`;
          case "assign":
            return `<assign variable="${name}" expression="${exp}"/>`;
          case "input":
            return `<input variable="${name}"/>`;
          case "output":
            return `<output expression="${exp}" newline="${node.newline ? "True" : "False"}"/>`;
          case "if":
            return `<if expression="${exp}"><then>${block(node.trueBranch ?? [])}</then><else>${block(node.falseBranch ?? [])}</else></if>`;
          case "while":
          case "do":
            return `<${node.kind} expression="${exp}">${block(node.body ?? [])}</${node.kind}>`;
          case "for":
            return `<for variable="${name}" start="${xml(node.start ?? "1")}" end="${xml(node.end ?? "5")}" direction="${node.direction}" step="${xml(node.step ?? "1")}">${block(node.body ?? [])}</for>`;
          case "comment":
            return `<comment text="${exp}"/>`;
          case "breakpoint":
            return "<breakpoint/>";
        }
      })
      .join("\n");
  return `<?xml version="1.0" encoding="utf-8"?>\n<flowgorithm fileversion="2.18"><attributes><attribute name="name" value="MedlegHub"/></attributes><function name="Main" type="None" variable=""><parameters/><body>${block(program.nodes)}</body></function></flowgorithm>`;
}
