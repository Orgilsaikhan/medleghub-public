import type { FlowNode, FlowProgram, InsertPoint } from "./model";

export interface ShapePosition {
  node: FlowNode;
  x: number;
  y: number;
  width: number;
  height: number;
}
export interface Wire {
  d: string;
  arrow?: boolean;
}
export interface Connector {
  x: number;
  y: number;
  point: InsertPoint;
}
export interface ChartLayout {
  shapes: ShapePosition[];
  wires: Wire[];
  connectors: Connector[];
  labels: { x: number; y: number; text: string }[];
  width: number;
  height: number;
  center: number;
  endY: number;
}

const sequenceWidth = (nodes: FlowNode[]): number => Math.max(240, ...nodes.map(nodeWidth));
function nodeWidth(node: FlowNode): number {
  if (node.kind === "if")
    return 2 * Math.max(sequenceWidth(node.trueBranch!), sequenceWidth(node.falseBranch!)) + 64;
  if (node.body) return sequenceWidth(node.body) + 144;
  return 240;
}

/** Structured layout keeps both branches and loop return paths connected after edits. */
export function layoutProgram(program: FlowProgram): ChartLayout {
  const width = sequenceWidth(program.nodes) + 64;
  const result: ChartLayout = {
    shapes: [],
    wires: [],
    connectors: [],
    labels: [],
    width,
    height: 0,
    center: width / 2,
    endY: 0,
  };
  const wire = (d: string, arrow = false) => result.wires.push({ d, arrow });
  const label = (x: number, y: number, text: string) => result.labels.push({ x, y, text });
  const sequence = (
    nodes: FlowNode[],
    x: number,
    startY: number,
    ownerId: string | null,
    branch: InsertPoint["branch"],
  ): number => {
    let y = startY;
    for (let index = 0; index <= nodes.length; index++) {
      wire(`M${x} ${y}V${y + 44}`, true);
      result.connectors.push({ x, y: y + 22, point: { ownerId, branch, index } });
      y += 44;
      if (index < nodes.length) y = statement(nodes[index], x, y);
    }
    return y;
  };
  const statement = (node: FlowNode, x: number, top: number): number => {
    const isIf = node.kind === "if";
    const isLoop = ["while", "for", "do"].includes(node.kind);
    const height = isIf ? 80 : isLoop ? 64 : 48;
    if (node.kind === "do") {
      const bodyEnd = sequence(node.body!, x, top, node.id, "body");
      result.shapes.push({ node, x, y: bodyEnd, width: 172, height });
      const left = x - nodeWidth(node) / 2 + 16;
      wire(`M${x - 86} ${bodyEnd + height / 2}H${left}V${top}H${x}`, true);
      label(left + 20, bodyEnd + height / 2 - 10, "True");
      label(x + 24, bodyEnd + height + 20, "False");
      return bodyEnd + height;
    }
    result.shapes.push({ node, x, y: top, width: isIf ? 184 : 172, height });
    if (isIf) {
      const branchWidth = Math.max(
        sequenceWidth(node.trueBranch!),
        sequenceWidth(node.falseBranch!),
      );
      const left = x - (branchWidth + 64) / 2;
      const right = x + (branchWidth + 64) / 2;
      const start = top + height / 2;
      wire(`M${x - 92} ${start}H${left}`);
      wire(`M${x + 92} ${start}H${right}`);
      label(left, start - 10, "True");
      label(right, start - 10, "False");
      const leftEnd = sequence(node.trueBranch!, left, start, node.id, "trueBranch");
      const rightEnd = sequence(node.falseBranch!, right, start, node.id, "falseBranch");
      const join = Math.max(leftEnd, rightEnd, top + height) + 18;
      wire(`M${left} ${leftEnd}V${join}H${right}V${rightEnd}`);
      return join;
    }
    if (isLoop) {
      const halfWidth = nodeWidth(node) / 2 - 16;
      label(x + 26, top + height + 16, "True");
      const bottom = sequence(node.body!, x, top + height, node.id, "body");
      wire(`M${x} ${bottom}H${x - halfWidth}V${top + height / 2}H${x - 86}`, true);
      const exit = bottom + 38;
      wire(`M${x + 86} ${top + height / 2}H${x + halfWidth}V${exit}H${x}`);
      label(x + halfWidth - 22, top + height / 2 - 10, "False");
      return exit;
    }
    return top + height;
  };
  result.endY = sequence(program.nodes, result.center, 64, null, "nodes");
  result.height = result.endY + 76;
  return result;
}
