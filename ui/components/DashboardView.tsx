"use client";

import React from "react";
import { Film, AlertTriangle, Eye, FileText, Video, RefreshCw } from "lucide-react";
import type { Alert, DashboardStats } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Badge, severityVariant } from "@/components/ui/Badge";
import { ConfidenceBar } from "@/components/ui/ConfidenceRing";

// ─── fallback stats when backend is offline ───────────────────────────────
const FALLBACK_STATS: DashboardStats = {
  cuts_analyzed: 142,
  retake_required: 1,
  director_review: 2,
  script_compliance: 99.2,
  production_title: "Night of the Living Dead (1968)",
  scene_range: "Scene 12–16 Farmhouse Siege",
  timecode_range: "25:00 – 45:00",
};

interface StatusCardProps {
  label: string;
  value: string | number;
  sub: string;
  icon: React.ReactNode;
  glow?: "cyan" | "critical" | "warning" | "success" | false;
  accent?: string;
}

function StatusCard({ label, value, sub, icon, glow = false, accent = "text-text-primary" }: StatusCardProps) {
  return (
    <Card glow={glow} className="p-5 relative overflow-hidden">
      {glow === "critical" && (
        <div className="absolute top-0 right-0 w-20 h-20 bg-severity-critical/10 rounded-bl-full pointer-events-none" />
      )}
      <div className="flex justify-between items-center text-text-secondary text-xs mb-2">
        <span>{label}</span>
        <span className="opacity-80">{icon}</span>
      </div>
      <div className={["text-3xl font-bold leading-none tabular-nums", accent].join(" ")}>{value}</div>
      <div className="text-[11px] text-text-secondary mt-2 leading-snug">{sub}</div>
    </Card>
  );
}

interface DashboardViewProps {
  alerts: Alert[];
  stats: DashboardStats | null;
  loadingAlerts: boolean;
  onRefresh: () => void;
  onSelectAlert: (a: Alert) => void;
  onNavigateToAlerts: () => void;
}

export default function DashboardView({
  alerts,
  stats,
  loadingAlerts,
  onRefresh,
  onSelectAlert,
  onNavigateToAlerts,
}: DashboardViewProps) {
  const s = stats ?? FALLBACK_STATS;

  const criticalAlerts = alerts.filter(
    (a) => a.director_action_required === "RETAKE REQUIRED" || a.severity === "critical"
  );
  const reviewAlerts = alerts.filter(
    (a) => a.director_action_required === "DIRECTOR REVIEW REQUIRED" || a.severity === "warning"
  );

  return (
    <div className="space-y-6">
      {/* ── Status Cards ─────────────────────────────────────────── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatusCard
          label="Cuts Analyzed"
          value={s.cuts_analyzed}
          sub={s.scene_range}
          icon={<Film className="w-4 h-4 text-accent-cyan" />}
          glow={false}
          accent="text-text-primary"
        />
        <StatusCard
          label="Retake Required"
          value={criticalAlerts.length || s.retake_required}
          sub={criticalAlerts[0]?.timestamp_film ? `${criticalAlerts[0].timestamp_film} flagged` : "37:08 'UPPER RIGHT CORNER'"}
          icon={<AlertTriangle className="w-4 h-4 text-severity-critical" />}
          glow="critical"
          accent="text-severity-critical"
        />
        <StatusCard
          label="Director Review"
          value={reviewAlerts.length || s.director_review}
          sub="Lighter Fluid & Footwear"
          icon={<Eye className="w-4 h-4 text-severity-warning" />}
          glow="warning"
          accent="text-severity-warning"
        />
        <StatusCard
          label="Script Compliance"
          value={`${s.script_compliance <= 1 ? (s.script_compliance * 100).toFixed(1) : s.script_compliance}%`}
          sub="Table action modified"
          icon={<FileText className="w-4 h-4 text-accent-cyan" />}
          glow={false}
          accent="text-accent-cyan"
        />
      </div>

      {/* ── Take Monitor + Alert Feed ─────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Video Monitor */}
        <Card className="lg:col-span-2 flex flex-col">
          <div className="flex items-center justify-between px-5 py-4 border-b border-border-subtle">
            <div className="flex items-center gap-2">
              <Video className="w-4 h-4 text-accent-cyan" />
              <h3 className="text-sm font-semibold">Take Monitor — {s.scene_range}</h3>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-text-secondary">{s.timecode_range}</span>
              <button
                onClick={onRefresh}
                className="flex items-center gap-1.5 text-xs bg-bg-elevated hover:bg-[#222230] border border-border-subtle px-3 py-1.5 rounded-lg text-text-secondary hover:text-text-primary transition"
              >
                <RefreshCw className={["w-3 h-3", loadingAlerts ? "animate-spin text-accent-cyan" : ""].join(" ")} />
                Sync
              </button>
            </div>
          </div>

          {/* Monitor canvas */}
          <div className="m-5 rounded-lg aspect-video bg-black flex flex-col items-center justify-center border border-border-subtle relative overflow-hidden">
            {/* Real Film Frame Image */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img 
              src="/evidence_frames/03_set_door_barricade_wide_0230.jpg" 
              alt="Take Monitor Live Feed" 
              className="absolute inset-0 w-full h-full object-cover opacity-85"
            />
            {/* Scanline overlay */}
            <div className="absolute inset-0 pointer-events-none" style={{
              backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px)",
            }} />
            {/* Critical banner */}
            {(criticalAlerts.length > 0 || s.retake_required > 0) && (
              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/95 via-black/70 to-transparent px-5 pt-8 pb-4">
                <div className="text-[11px] text-severity-critical font-mono font-bold mb-1 animate-pulse">
                  🚨 RETAKE REQUIRED — {criticalAlerts[0]?.timestamp_film || "37:08"} · 100% CONFIDENCE
                </div>
                <div className="text-sm font-semibold text-white">
                  {criticalAlerts[0]?.title || "Visible Crew Handwriting on Barricade Plank: 'UPPER RIGHT CORNER'"}
                </div>
              </div>
            )}

            {/* Timecode HUD */}
            <div className="absolute top-3 left-3 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-severity-critical animate-pulse" />
              <span className="text-[11px] font-mono text-severity-critical">REC</span>
              <span className="text-[11px] font-mono text-text-secondary ml-2">37:08:14</span>
            </div>
          </div>

          {/* Confidence strip */}
          <div className="px-5 pb-5 space-y-2">
            <p className="text-[11px] text-text-secondary font-mono uppercase">Model Confidence — Active Flags</p>
            {alerts.slice(0, 3).map((a, i) => (
              <ConfidenceBar key={i} value={a.confidence} label={a.title.slice(0, 50)} />
            ))}
            {alerts.length === 0 && (
              <>
                <ConfidenceBar value={1.0} label="Crew marking on barricade plank ('UPPER RIGHT CORNER')" />
                <ConfidenceBar value={0.92} label="Charcoal Lighter Fluid container position continuity" />
                <ConfidenceBar value={0.88} label="Barbra footwear state between cuts" />
              </>
            )}
          </div>
        </Card>

        {/* Alert Queue */}
        <Card className="flex flex-col">
          <div className="flex items-center justify-between px-5 py-4 border-b border-border-subtle">
            <h3 className="text-sm font-semibold">Continuity Queue</h3>
            <span className="text-xs text-accent-cyan font-mono">{alerts.length || 4} items</span>
          </div>
          <div className="flex-1 overflow-y-auto p-3 space-y-2.5 max-h-[420px]">
            {(alerts.length > 0 ? alerts : FALLBACK_ALERTS).map((al, idx) => (
              <button
                key={al.alert_id || idx}
                onClick={() => { onSelectAlert(al); onNavigateToAlerts(); }}
                className={[
                  "w-full text-left p-3 rounded-lg border transition group",
                  al.director_action_required === "RETAKE REQUIRED"
                    ? "bg-severity-critical/10 border-severity-critical/40 hover:border-severity-critical"
                    : "bg-[#1a1a24] border-border-subtle hover:border-text-muted",
                ].join(" ")}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <Badge
                    variant={severityVariant(al.director_action_required || al.severity)}
                    pulse={al.director_action_required === "RETAKE REQUIRED"}
                  >
                    {al.director_action_required === "RETAKE REQUIRED"
                      ? "Retake"
                      : al.director_action_required === "DIRECTOR REVIEW REQUIRED"
                      ? "Review"
                      : "Logged"}
                  </Badge>
                  <span className="text-[10px] font-mono text-text-secondary">{al.timestamp_film}</span>
                </div>
                <p className="text-xs font-semibold text-text-primary line-clamp-1">{al.title}</p>
                <p className="text-[11px] text-text-secondary line-clamp-2 mt-0.5">
                  {al.visual_evidence || al.description}
                </p>
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

// Fallback data so the dashboard renders without a backend
const FALLBACK_ALERTS: Alert[] = [
  {
    alert_id: "alert_001",
    take_id: "s12_sh03_t04",
    scene: 12,
    category: "Production Error",
    severity: "critical",
    confidence: 1.0,
    title: "Visible Crew Marking 'UPPER RIGHT CORNER' on Barricade",
    description: "A crew handwriting production note is legible in frame at 37:08.",
    visual_evidence: "White chalk text clearly visible on wooden plank during boarding scene.",
    director_action_required: "RETAKE REQUIRED",
    timestamp_film: "37:08",
  },
  {
    alert_id: "alert_002",
    take_id: "s13_sh01_t02",
    scene: 13,
    category: "Prop Continuity",
    severity: "warning",
    confidence: 0.92,
    title: "Charcoal Lighter Fluid Container Position",
    description: "Container moved between cuts without scripted action.",
    visual_evidence: "Position inconsistency across Scene 13 cut points.",
    director_action_required: "DIRECTOR REVIEW REQUIRED",
    timestamp_film: "31:22",
  },
  {
    alert_id: "alert_003",
    take_id: "s14_sh02_t01",
    scene: 14,
    category: "Wardrobe",
    severity: "warning",
    confidence: 0.88,
    title: "Barbra Footwear State Change",
    description: "Shoes present in Shot 2, absent in Shot 5 without scripted removal.",
    director_action_required: "DIRECTOR REVIEW REQUIRED",
    timestamp_film: "38:44",
  },
  {
    alert_id: "alert_004",
    take_id: "s16_sh01_t03",
    scene: 16,
    category: "Script Compliance",
    severity: "info",
    confidence: 0.75,
    title: "Ben Table Disassembly Sequence Modified",
    description: "Actor improvised method; script specifies systematic leg removal.",
    director_action_required: "LOGGED",
    timestamp_film: "42:15",
  },
];
