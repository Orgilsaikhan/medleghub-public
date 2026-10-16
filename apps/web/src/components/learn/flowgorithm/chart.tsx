"use client";

import { useId, useMemo } from "react";
import { layoutProgram } from "@/lib/flowgorithm/layout";
import {
  isIncomplete,
  LABELS,
  nodeText,
  type FlowNode,
  type FlowProgram,
  type InsertPoint,
} from "@/lib/flowgorithm/model";
import { Shape } from "./shape";

export function Chart({
  program,
  zoom,
  activeId,
  locked,
  onEdit,
  onInsert,
}: {
  program: FlowProgram;
  zoom: number;
  activeId: string | null;
  locked: boolean;
  onEdit: (node: FlowNode) => void;
  onInsert: (point: InsertPoint) => void;
}) {
  const layout = useMemo(() => layoutProgram(program), [program]);
  const arrowId = useId().replace(/:/g, "");
  const terminal = (label: string, y: number) => (
    <foreignObject x={layout.center - 64} y={y} width={128} height={44}>
      <div className="relative flex h-full items-center justify-center text-sm text-slate-950">
        <Shape kind="terminal" />
        <span className="relative">{label}</span>
      </div>
    </foreignObject>
  );
  return (
    <div
      className="min-h-0 min-w-0 flex-1 overflow-auto bg-white p-5"
      role="region"
      aria-label="Блок схем"
      tabIndex={0}
    >
      <svg
        width={layout.width * zoom}
        height={layout.height * zoom}
        viewBox={`0 0 ${layout.width} ${layout.height}`}
        className="mx-auto block max-w-none"
        aria-label="Main-аас End хүртэлх алгоритм"
      >
        <defs>
          <marker id={arrowId} markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
            <path d="M0 0L7 3.5L0 7Z" fill="#dd814c" />
          </marker>
        </defs>
        {layout.wires.map((wire, index) => (
          <path
            key={index}
            d={wire.d}
            fill="none"
            stroke="#dd814c"
            strokeWidth="1.5"
            markerEnd={wire.arrow ? `url(#${arrowId})` : undefined}
          />
        ))}
        {layout.labels.map((label, index) => (
          <text
            key={index}
            x={label.x}
            y={label.y}
            textAnchor="middle"
            fill="#6b7280"
            fontSize="11"
          >
            {label.text}
          </text>
        ))}
        {terminal("Main", 20)}
        {layout.shapes.map(({ node, x, y, width, height }) => (
          <foreignObject key={node.id} x={x - width / 2} y={y} width={width} height={height}>
            <button
              type="button"
              disabled={locked}
              data-node-id={node.id}
              data-node-kind={node.kind}
              data-active={activeId === node.id}
              aria-label={`${LABELS[node.kind]}: ${isIncomplete(node) ? "утга оруулаагүй" : nodeText(node)}`}
              title={nodeText(node)}
              onClick={() => onEdit(node)}
              className="relative flex h-full w-full items-center justify-center px-7 text-center text-[12px] leading-tight text-slate-950 outline-none hover:brightness-95 focus-visible:ring-2 focus-visible:ring-orange-600 focus-visible:ring-inset disabled:cursor-default"
            >
              <Shape kind={node.kind} active={activeId === node.id} />
              <span className="relative z-10 line-clamp-3 break-words">{nodeText(node)}</span>
            </button>
          </foreignObject>
        ))}
        {layout.connectors.map(({ x, y, point }, index) => (
          <foreignObject key={index} x={x - 15} y={y - 15} width={30} height={30}>
            <button
              type="button"
              disabled={locked}
              aria-label={`Дүрс нэмэх: ${point.ownerId ? `${point.branch} ` : "Main "}${point.index + 1}`}
              title="Энд дүрс нэмэх"
              onClick={() => onInsert(point)}
              className="flex size-[30px] items-center justify-center rounded-full border border-transparent bg-white/85 text-lg text-orange-700 hover:border-orange-300 hover:bg-orange-100 focus-visible:outline-2 focus-visible:outline-orange-600 disabled:invisible"
            >
              +
            </button>
          </foreignObject>
        ))}
        {terminal("End", layout.endY)}
      </svg>
    </div>
  );
}
