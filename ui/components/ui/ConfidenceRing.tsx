import React from "react";

interface ConfidenceRingProps {
  value: number; // 0–1
  size?: number;
  strokeWidth?: number;
}

export function ConfidenceRing({ value, size = 72, strokeWidth = 5 }: ConfidenceRingProps) {
  const pct = Math.min(Math.max(value, 0), 1);
  const r = (size - strokeWidth * 2) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - pct);
  const pctInt = Math.round(pct * 100);

  const color =
    pct >= 0.85 ? "#ff3366" :
    pct >= 0.65 ? "#ffaa33" :
    "#00d4ff";

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke="#2a2a3a" strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke={color} strokeWidth={strokeWidth}
          strokeDasharray={circ} strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
      </svg>
      <span
        className="absolute text-sm font-bold font-mono"
        style={{ color }}
      >
        {pctInt}%
      </span>
    </div>
  );
}

interface ConfidenceBarProps {
  value: number;
  label?: string;
}

export function ConfidenceBar({ value, label }: ConfidenceBarProps) {
  const pct = Math.round(Math.min(Math.max(value, 0), 1) * 100);
  const color =
    pct >= 85 ? "bg-severity-critical" :
    pct >= 65 ? "bg-severity-warning" :
    "bg-accent-cyan";

  return (
    <div className="space-y-1">
      {label && (
        <div className="flex justify-between text-[11px] font-mono">
          <span className="text-text-secondary">{label}</span>
          <span className="text-text-primary">{pct}%</span>
        </div>
      )}
      <div className="h-1.5 bg-border-subtle rounded-full overflow-hidden">
        <div
          className={[color, "h-full rounded-full transition-all duration-700"].join(" ")}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
