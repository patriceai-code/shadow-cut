"use client";

import React from "react";
import { TrendingUp, Cpu, ShieldCheck, Film, AlertTriangle, BarChart2 } from "lucide-react";
import type { TrustReport } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

// ─── Helpers ───────────────────────────────────────────────────────────────

function fmt(n: number, prefix = "", suffix = "", decimals = 0): string {
  return `${prefix}${n.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}${suffix}`;
}

// ─── Hero Metric Card ─────────────────────────────────────────────────────

interface HeroCardProps {
  label: string;
  value: string;
  sub: string;
  icon: React.ReactNode;
  iconBg: string;
  valueColor: string;
}

function HeroCard({ label, value, sub, icon, iconBg, valueColor }: HeroCardProps) {
  return (
    <div className="bg-bg-secondary border border-border-subtle rounded-xl p-6 flex flex-col gap-3">
      <div className={["w-10 h-10 rounded-lg flex items-center justify-center", iconBg].join(" ")}>
        {icon}
      </div>
      <div>
        <p className="text-[11px] font-mono text-text-secondary uppercase tracking-wider">{label}</p>
        <p className={["text-4xl font-bold tabular-nums mt-1 leading-none", valueColor].join(" ")}>{value}</p>
      </div>
      <p className="text-xs text-text-secondary leading-snug">{sub}</p>
    </div>
  );
}

// ─── Accuracy Bar ─────────────────────────────────────────────────────────

interface MetricRowProps {
  label: string;
  value: number;
  max?: number;
  unit?: string;
  color?: string;
}

function MetricRow({ label, value, max = 100, unit = "%", color = "bg-accent-cyan" }: MetricRowProps) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div className="space-y-1.5">
      <div className="flex justify-between items-center text-xs">
        <span className="text-text-secondary">{label}</span>
        <span className="font-mono text-text-primary font-semibold tabular-nums">
          {typeof value === "number" && unit === "%" ? `${value}${unit}` : `${value}`}
        </span>
      </div>
      <div className="h-2 bg-border-subtle rounded-full overflow-hidden">
        <div
          className={[color, "h-full rounded-full transition-all duration-700"].join(" ")}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

// ─── Trust Report View ────────────────────────────────────────────────────

interface TrustReportViewProps {
  report: TrustReport | null;
}

const FALLBACK: TrustReport = {
  production_title: "Night of the Living Dead (1968)",
  scene_range: "Scene 12–16 Farmhouse Siege",
  reshoot_savings_usd: 45_000,
  compute_cost_usd: 0.046,
  director_autonomy_pct: 100,
  cuts_analyzed: 142,
  retakes_caught: 1,
  accuracy_pct: 98.4,
  executive_verdict:
    "Comprehensive audit of the 20-minute Farmhouse Siege sequence reveals several notable script deviations and a severe production continuity error. Most critically, an unmasked production marking ('UPPER RIGHT CORNER') is visibly written on a reinforcement wood plank during the living room boarding scene at 37:08 — confirmed at 100% confidence by both YOLO detection and Gemini validation. Wardrobe and prop tracking show occasional discrepancies, notably Barbra's footwear state change and the Charcoal Lighter Fluid container position across cuts. Script compliance is at 99.2%, with Ben's table disassembly sequence being the most notable physical performance deviation from the Romero/Russo shooting screenplay.",
  date: "2026-09-04",
};

export default function TrustReportView({ report }: TrustReportViewProps) {
  const r = report ?? FALLBACK;

  const roi = r.compute_cost_usd > 0
    ? Math.round(r.reshoot_savings_usd / r.compute_cost_usd)
    : 0;

  return (
    <div className="space-y-6">
      {/* Report header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-text-primary">Director's Daily Trust Report</h2>
          <p className="text-xs text-text-secondary mt-1">
            {r.production_title} · {r.scene_range}
            {r.date && <span className="ml-2 opacity-60">· {r.date}</span>}
          </p>
        </div>
        <Badge variant="success" className="text-xs px-3 py-1">Script-Grounded Audit</Badge>
      </div>

      {/* ── Hero cards ─────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <HeroCard
          label="Estimated Reshoot Savings"
          value={fmt(r.reshoot_savings_usd, "$", "", 0)}
          sub={`${r.retakes_caught} retake caught · prevented 1 day of post-wrap pickups`}
          icon={<TrendingUp className="w-5 h-5 text-severity-success" />}
          iconBg="bg-severity-success/10 border border-severity-success/20"
          valueColor="text-severity-success"
        />
        <HeroCard
          label="Compute Cost (Gemini)"
          value={fmt(r.compute_cost_usd, "$", "", 3)}
          sub={`${r.cuts_analyzed} cuts · 20 min footage · ${fmt(roi, "", "× ROI")}`}
          icon={<Cpu className="w-5 h-5 text-accent-cyan" />}
          iconBg="bg-accent-cyan/10 border border-accent-cyan/20"
          valueColor="text-accent-cyan"
        />
        <HeroCard
          label="Director Autonomy"
          value={`${r.director_autonomy_pct}%`}
          sub="AI provides evidence only — every decision stays with the director"
          icon={<ShieldCheck className="w-5 h-5 text-text-secondary" />}
          iconBg="bg-border-subtle border border-border-subtle"
          valueColor="text-text-primary"
        />
      </div>

      {/* ── Accuracy & metrics ─────────────────────────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <div className="p-5 space-y-4">
            <h3 className="text-sm font-semibold flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-accent-cyan" />
              Detection Metrics
            </h3>
            <MetricRow label="Overall Accuracy" value={r.accuracy_pct} color="bg-severity-success" />
            <MetricRow label="Director Autonomy" value={r.director_autonomy_pct} color="bg-accent-cyan" />
            <MetricRow label="Script Compliance" value={99.2} color="bg-accent-cyan" />
          </div>
        </Card>

        <Card>
          <div className="p-5 space-y-4">
            <h3 className="text-sm font-semibold flex items-center gap-2">
              <Film className="w-4 h-4 text-accent-cyan" />
              Production Summary
            </h3>
            {[
              { label: "Cuts Analyzed", value: r.cuts_analyzed, color: "text-text-primary" },
              { label: "Retakes Caught", value: r.retakes_caught, color: "text-severity-critical" },
              { label: "Director Reviews", value: 2, color: "text-severity-warning" },
              { label: "Silently Logged", value: 1, color: "text-text-secondary" },
            ].map((row) => (
              <div key={row.label} className="flex items-center justify-between text-sm border-b border-border-subtle pb-2 last:border-0 last:pb-0">
                <span className="text-text-secondary">{row.label}</span>
                <span className={["font-bold tabular-nums font-mono", row.color].join(" ")}>{row.value}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* ── Cost efficiency callout ──────────────────────────────────── */}
      <div className="rounded-xl border border-severity-success/30 bg-severity-success/5 p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <TrendingUp className="w-8 h-8 text-severity-success shrink-0" />
          <div>
            <p className="text-sm font-bold text-text-primary">
              {fmt(roi, "", "× return on AI investment")}
            </p>
            <p className="text-xs text-text-secondary mt-0.5">
              {fmt(r.reshoot_savings_usd, "$")} saved · {fmt(r.compute_cost_usd, "$", "", 3)} spent
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono text-severity-success">
          <AlertTriangle className="w-4 h-4" />
          <span>1 retake flagged at 100% confidence</span>
        </div>
      </div>

      {/* ── Executive verdict ────────────────────────────────────────── */}
      <Card>
        <div className="p-5">
          <h3 className="text-sm font-semibold text-text-primary mb-3">Executive Verdict</h3>
          <p className="text-sm text-text-secondary leading-relaxed">{r.executive_verdict}</p>
        </div>
      </Card>
    </div>
  );
}
