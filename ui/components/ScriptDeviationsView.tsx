"use client";

import React, { useState } from "react";
import { FileText, ChevronDown, ChevronUp } from "lucide-react";
import type { ScriptDeviation } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

// ─── Individual deviation card ─────────────────────────────────────────────

interface DeviationCardProps {
  deviation: ScriptDeviation;
  index: number;
}

function DeviationCard({ deviation, index }: DeviationCardProps) {
  const [expanded, setExpanded] = useState(index === 0);

  const severityVariant =
    deviation.severity === "critical"
      ? "critical"
      : deviation.severity === "warning"
      ? "warning"
      : "muted";

  return (
    <Card
      glow={deviation.severity === "critical" ? "critical" : deviation.severity === "warning" ? "warning" : false}
      className="overflow-hidden"
    >
      {/* Header row */}
      <button
        className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-white/[0.02] transition"
        onClick={() => setExpanded((v) => !v)}
      >
        <div className="flex items-center gap-3 min-w-0">
          <span className="text-[11px] font-mono text-accent-cyan shrink-0">
            {deviation.timestamp_film}
          </span>
          {deviation.character && (
            <span className="text-[11px] text-text-secondary shrink-0">
              {deviation.character}
            </span>
          )}
          <Badge variant={severityVariant}>{deviation.severity}</Badge>
          {deviation.scene_number && (
            <span className="text-[10px] font-mono text-text-muted">Scene {deviation.scene_number}</span>
          )}
        </div>
        <div className="flex items-center gap-2 shrink-0 ml-4">
          <span className="text-[11px] text-text-secondary hidden sm:block">
            {expanded ? "Collapse" : "Expand"}
          </span>
          {expanded ? (
            <ChevronUp className="w-4 h-4 text-text-secondary" />
          ) : (
            <ChevronDown className="w-4 h-4 text-text-secondary" />
          )}
        </div>
      </button>

      {/* Collapsible body */}
      {expanded && (
        <div className="px-5 pb-5 space-y-4 border-t border-border-subtle">
          {/* Side-by-side comparison */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
            {/* Written screenplay */}
            <div className="rounded-lg border border-border-subtle bg-bg-primary p-4 flex flex-col gap-2">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-text-secondary" />
                <span className="text-[10px] font-mono text-text-secondary uppercase tracking-wider">
                  Written in Screenplay
                </span>
              </div>
              <p className="text-sm text-text-primary leading-relaxed font-medium">
                {deviation.scripted_element}
              </p>
            </div>

            {/* Filmed performance */}
            <div className="rounded-lg border border-severity-success/30 bg-severity-success/5 p-4 flex flex-col gap-2">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-severity-success" />
                <span className="text-[10px] font-mono text-severity-success uppercase tracking-wider">
                  Performed on Camera
                </span>
              </div>
              <p className="text-sm text-text-primary leading-relaxed">
                {deviation.filmed_reality}
              </p>
            </div>
          </div>

          {/* Impact note */}
          <div className="flex gap-2 items-start bg-[#1a1a24] border border-border-subtle rounded-lg px-4 py-3">
            <span className="text-severity-warning mt-0.5 shrink-0">⚑</span>
            <p className="text-xs text-text-secondary italic leading-relaxed">{deviation.objective_impact}</p>
          </div>
        </div>
      )}
    </Card>
  );
}

// ─── Script Deviations View ────────────────────────────────────────────────

interface ScriptDeviationsViewProps {
  deviations: ScriptDeviation[];
}

export default function ScriptDeviationsView({ deviations }: ScriptDeviationsViewProps) {
  const display = deviations.length > 0 ? deviations : FALLBACK_DEVIATIONS;
  const critCount = display.filter((d) => d.severity === "critical").length;
  const warnCount = display.filter((d) => d.severity === "warning").length;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-text-primary flex items-center gap-2">
            <FileText className="w-5 h-5 text-accent-cyan" />
            Screenplay vs Filmed Performance
          </h2>
          <p className="text-xs text-text-secondary mt-1">
            Grounded cross-reference · Romero &amp; Russo (1968) Shooting Screenplay
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="cyan" className="text-xs px-3 py-1">Script Audit Active</Badge>
          {critCount > 0 && (
            <Badge variant="critical">{critCount} critical</Badge>
          )}
          {warnCount > 0 && (
            <Badge variant="warning">{warnCount} warning</Badge>
          )}
        </div>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Deviations Found", value: display.length, color: "text-text-primary" },
          { label: "Affect Continuity", value: display.filter(d => d.severity !== "info").length, color: "text-severity-warning" },
          { label: "Require Retake", value: critCount, color: "text-severity-critical" },
        ].map((stat) => (
          <div key={stat.label} className="bg-bg-secondary border border-border-subtle rounded-xl p-4 text-center">
            <div className={["text-2xl font-bold tabular-nums", stat.color].join(" ")}>{stat.value}</div>
            <div className="text-[11px] text-text-secondary mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Cards */}
      <div className="space-y-3">
        {display.map((dev, idx) => (
          <DeviationCard key={idx} deviation={dev} index={idx} />
        ))}
      </div>
    </div>
  );
}

// ─── Fallback data ──────────────────────────────────────────────────────────

const FALLBACK_DEVIATIONS: ScriptDeviation[] = [
  {
    timestamp_film: "42:15",
    character: "Ben",
    scene_number: 16,
    severity: "warning",
    scripted_element:
      "Ben removes each leg of the wooden table individually, stacking them against the door methodically while maintaining eye contact with the approaching dead.",
    filmed_reality:
      "Ben overturns the entire table in one motion, then breaks it apart by stamping on it. The individual leg removal is skipped. He does not maintain eye contact with the threat during this action.",
    objective_impact:
      "The scripted method emphasises Ben's strategic, composed nature under pressure. The filmed improvisation reads as more desperate and chaotic — a tonal deviation that may affect character consistency across scenes.",
  },
  {
    timestamp_film: "29:40",
    character: "Barbra",
    scene_number: 12,
    severity: "info",
    scripted_element:
      "Barbra sits motionless in the armchair, staring at the front door. No dialogue. Script direction: 'She is in shock, completely dissociated.'",
    filmed_reality:
      "Barbra rocks slightly and mouths words inaudibly. Actress adds subtle physical performance — not scripted but consistent with character state.",
    objective_impact:
      "Minor addition that enriches character without contradicting narrative. Logged for director awareness only; no continuity concern.",
  },
  {
    timestamp_film: "33:55",
    character: "Harry",
    scene_number: 14,
    severity: "warning",
    scripted_element:
      "Harry says: 'If you'd have listened to me from the beginning, none of this would have happened.' Accusatory tone, pointing at Ben.",
    filmed_reality:
      "Actor delivers the line without the pointing gesture. Tone is more resigned than accusatory. The confrontational blocking written in the script is absent.",
    objective_impact:
      "Reduces the escalation of the Harry/Ben conflict. May weaken the emotional payoff of their later confrontation if the audience hasn't seen sufficient tension build-up.",
  },
];
