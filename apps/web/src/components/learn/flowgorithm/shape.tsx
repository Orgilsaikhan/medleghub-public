import type { NodeKind } from "@/lib/flowgorithm/model";

export function Shape({ kind, active = false }: { kind: NodeKind | "terminal"; active?: boolean }) {
  const palette =
    kind === "terminal"
      ? ["#f0e0ff", "#9474ac"]
      : kind === "input"
        ? ["#cfe5ff", "#7396b5"]
        : kind === "output"
          ? ["#d7ffd7", "#78a178"]
          : kind === "if"
            ? ["#ffd9d9", "#b17c7c"]
            : ["while", "for", "do"].includes(kind)
              ? ["#ffe2b0", "#b28b53"]
              : kind === "breakpoint"
                ? ["#ffaaaa", "#b55b5b"]
                : kind === "comment"
                  ? ["#ffffff", "#777777"]
                  : ["#ffffd9", "#a0a078"];
  const stroke = active ? "#e87916" : palette[1];
  const common = {
    fill: palette[0],
    stroke,
    strokeWidth: active ? 3 : 1.2,
    vectorEffect: "non-scaling-stroke" as const,
  };
  return (
    <svg
      viewBox="0 0 180 60"
      preserveAspectRatio="none"
      className="absolute inset-0 h-full w-full"
      aria-hidden
    >
      {kind === "terminal" ? (
        <rect x="2" y="2" width="176" height="56" rx="28" {...common} />
      ) : kind === "if" ? (
        <polygon points="90,2 178,30 90,58 2,30" {...common} />
      ) : ["while", "for", "do"].includes(kind) ? (
        <polygon points="25,2 155,2 178,30 155,58 25,58 2,30" {...common} />
      ) : kind === "input" || kind === "output" ? (
        <polygon points="27,2 178,2 153,58 2,58" {...common} />
      ) : kind === "breakpoint" ? (
        <polygon points="57,2 123,2 148,20 148,40 123,58 57,58 32,40 32,20" {...common} />
      ) : (
        <rect
          x="2"
          y="2"
          width="176"
          height="56"
          {...common}
          strokeDasharray={kind === "comment" ? "4 3" : undefined}
        />
      )}
      {kind === "declare" && (
        <path
          d="M16 2V58M2 13H178"
          fill="none"
          stroke={stroke}
          strokeWidth="1"
          vectorEffect="non-scaling-stroke"
        />
      )}
    </svg>
  );
}
