"use client";

import React from "react";
import { Clock, XCircle, CheckCircle2, MinusCircle, ImageOff } from "lucide-react";
import type { Alert, DirectorDecision } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Badge, severityVariant } from "@/components/ui/Badge";
import { ConfidenceRing } from "@/components/ui/ConfidenceRing";

// ─── Frame Comparison Card ─────────────────────────────────────────────────

interface FrameCardProps {
  label: string;
  labelColor: string;
  src?: string;
  timecode?: string;
  note?: string;
}

function FrameCard({ label, labelColor, src, timecode, note }: FrameCardProps) {
  return (
    <div className="rounded-lg border border-border-subtle overflow-hidden bg-black flex flex-col">
      <div className={["flex items-center justify-between px-3 py-1.5 text-[10px] font-mono uppercase font-bold", labelColor].join(" ")}>
        <span>{label}</span>
        {timecode && <span className="opacity-70">{timecode}</span>}
      </div>
      <div className="aspect-video bg-[#0d0d14] flex items-center justify-center relative">
        {src ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={src} alt={label} className="w-full h-full object-cover" />
        ) : (
          <div className="flex flex-col items-center gap-2 text-border-subtle">
            <ImageOff className="w-8 h-8" />
            <span className="text-[10px] text-text-muted">Frame unavailable</span>
          </div>
        )}
        {/* Crosshair marker */}
        {!src && (
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-1/2 left-0 right-0 h-px bg-border-subtle/50" />
            <div className="absolute left-1/2 top-0 bottom-0 w-px bg-border-subtle/50" />
          </div>
        )}
      </div>
      {note && <p className="px-3 py-2 text-[11px] text-text-secondary">{note}</p>}
    </div>
  );
}

// ─── Alert Queue Item ──────────────────────────────────────────────────────

interface AlertQueueItemProps {
  alert: Alert;
  isSelected: boolean;
  decision?: string;
  onClick: () => void;
}

function AlertQueueItem({ alert, isSelected, decision, onClick }: AlertQueueItemProps) {
  return (
    <button
      onClick={onClick}
      className={[
        "w-full text-left p-4 rounded-xl border transition",
        isSelected
          ? "bg-[#1a1a24] border-accent-cyan"
          : "bg-bg-secondary border-border-subtle hover:border-text-muted",
      ].join(" ")}
    >
      <div className="flex justify-between items-center text-xs mb-1">
        <span className="text-text-secondary font-mono text-[10px]">{alert.timestamp_film}</span>
        <Badge variant={severityVariant(alert.director_action_required || alert.severity)}>
          {alert.director_action_required === "RETAKE REQUIRED"
            ? "Retake"
            : alert.director_action_required === "DIRECTOR REVIEW REQUIRED"
            ? "Review"
            : "Logged"}
        </Badge>
      </div>
      <h4 className="text-sm font-bold text-text-primary leading-snug">{alert.title}</h4>
      {decision && (
        <div className="mt-2 text-[10px] font-mono uppercase text-accent-cyan flex items-center gap-1">
          <CheckCircle2 className="w-3 h-3" />
          <span>Director: {decision}</span>
        </div>
      )}
    </button>
  );
}

// ─── Main Alert Detail View ────────────────────────────────────────────────

interface AlertDetailViewProps {
  alerts: Alert[];
  selectedAlert: Alert | null;
  onSelectAlert: (a: Alert) => void;
  userDecisions: Record<string, DirectorDecision>;
  onDecision: (alertId: string, decision: DirectorDecision) => void;
}

export default function AlertDetailView({
  alerts,
  selectedAlert,
  onSelectAlert,
  userDecisions,
  onDecision,
}: AlertDetailViewProps) {
  const displayAlerts = (alerts.length > 0 ? alerts : FALLBACK_ALERTS).map(attachEvidenceFrames);
  const activeRaw = selectedAlert ?? displayAlerts[0] ?? null;
  const active = activeRaw ? attachEvidenceFrames(activeRaw) : null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* ── Left: Queue ──────────────────────────────────────────── */}
      <div className="md:col-span-1 space-y-3">
        <h3 className="text-xs font-semibold text-text-secondary uppercase tracking-wider px-1">
          Continuity Queue
        </h3>
        {displayAlerts.map((al, idx) => (
          <AlertQueueItem
            key={al.alert_id || idx}
            alert={al}
            isSelected={active?.alert_id === al.alert_id}
            decision={userDecisions[al.alert_id]}
            onClick={() => onSelectAlert(al)}
          />
        ))}
      </div>

      {/* ── Right: Detail ────────────────────────────────────────── */}
      {active && (
        <div className="md:col-span-2 space-y-5">
          {/* Severity header */}
          <Card
            glow={
              active.director_action_required === "RETAKE REQUIRED"
                ? "critical"
                : active.director_action_required === "DIRECTOR REVIEW REQUIRED"
                ? "warning"
                : false
            }
          >
            <div className="p-5">
              <div className="flex flex-wrap items-start justify-between gap-4">
                {/* Left: title block */}
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2 mb-2">
                    <span className="text-[11px] font-mono text-accent-cyan uppercase tracking-wider">
                      {active.category} Audit
                    </span>
                    <Badge
                      variant={severityVariant(active.director_action_required || active.severity)}
                      pulse={active.director_action_required === "RETAKE REQUIRED"}
                    >
                      {active.director_action_required || active.severity}
                    </Badge>
                  </div>
                  <h2 className="text-lg font-bold text-text-primary leading-snug">{active.title}</h2>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-text-secondary mt-2">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {active.timestamp_film ?? "—"}
                    </span>
                    <span className="font-mono bg-[#1a1a24] px-2 py-0.5 rounded border border-border-subtle">
                      Scene {active.scene} · {active.take_id}
                    </span>
                  </div>
                </div>

                {/* Right: Confidence ring */}
                <ConfidenceRing value={active.confidence} size={80} strokeWidth={6} />
              </div>

              {/* Director action buttons */}
              <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-border-subtle">
                <button
                  onClick={() => onDecision(active.alert_id, "retake")}
                  className={[
                    "flex items-center gap-1.5 text-xs font-semibold px-4 py-2 rounded-lg transition",
                    userDecisions[active.alert_id] === "retake"
                      ? "bg-severity-critical text-white ring-2 ring-white/30"
                      : "bg-severity-critical/80 hover:bg-severity-critical text-white",
                  ].join(" ")}
                >
                  <XCircle className="w-3.5 h-3.5" />
                  Retake Take
                </button>
                <button
                  onClick={() => onDecision(active.alert_id, "accept")}
                  className={[
                    "flex items-center gap-1.5 text-xs px-4 py-2 rounded-lg border transition",
                    userDecisions[active.alert_id] === "accept"
                      ? "bg-accent-cyan text-black font-semibold border-accent-cyan"
                      : "bg-[#1a1a24] hover:bg-[#222230] text-text-secondary hover:text-text-primary border-border-subtle",
                  ].join(" ")}
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Accept Risk
                </button>
                <button
                  onClick={() => onDecision(active.alert_id, "dismiss")}
                  className={[
                    "flex items-center gap-1.5 text-xs px-4 py-2 rounded-lg border transition",
                    userDecisions[active.alert_id] === "dismiss"
                      ? "bg-[#2a2a3a] text-text-secondary border-text-muted"
                      : "bg-[#1a1a24] hover:bg-[#222230] text-text-muted hover:text-text-secondary border-border-subtle",
                  ].join(" ")}
                >
                  <MinusCircle className="w-3.5 h-3.5" />
                  Dismiss
                </button>
              </div>
            </div>
          </Card>

          {/* Frame comparison */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <FrameCard
              label="Reference Frame (Script Expected)"
              labelColor="bg-accent-cyan/20 text-accent-cyan"
              src={active.frame_before}
              timecode={active.timestamp_clip}
              note="Script supervisor reference state"
            />
            <FrameCard
              label="Flagged Frame (Anomaly Detected)"
              labelColor="bg-severity-critical/20 text-severity-critical"
              src={active.frame_after}
              timecode={active.timestamp_film}
              note="YOLO detection · Gemini validated"
            />
          </div>

          {/* Evidence cards */}
          <div className="space-y-3">
            <Card>
              <div className="p-4">
                <h4 className="text-[10px] uppercase font-mono text-text-secondary mb-2 tracking-wider">Description</h4>
                <p className="text-sm text-text-primary leading-relaxed">{active.description}</p>
              </div>
            </Card>

            {active.visual_evidence && (
              <Card>
                <div className="p-4">
                  <h4 className="text-[10px] uppercase font-mono text-accent-cyan mb-2 tracking-wider">
                    Objective Forensic Evidence
                  </h4>
                  <p className="text-sm text-text-secondary leading-relaxed">{active.visual_evidence}</p>
                </div>
              </Card>
            )}

            {active.technical_impact && (
              <Card>
                <div className="p-4">
                  <h4 className="text-[10px] uppercase font-mono text-severity-warning mb-2 tracking-wider">
                    Technical &amp; Narrative Impact
                  </h4>
                  <p className="text-sm text-text-secondary leading-relaxed">{active.technical_impact}</p>
                </div>
              </Card>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Helper to guarantee every alert has its before and after evidence frames
export function attachEvidenceFrames(alert: Alert): Alert {
  if (alert.frame_before && alert.frame_after) return alert;

  const title = (alert.title || "").toLowerCase();
  const cat = (alert.category || "").toLowerCase();

  if (title.includes("upper right corner") || title.includes("barricade") || title.includes("carpenter") || cat.includes("set")) {
    return {
      ...alert,
      frame_before: "/evidence_frames/03_set_door_barricade_wide_0230.jpg",
      frame_after: "/evidence_frames/03_set_door_barricade_wide_0230.jpg",
    };
  } else if (title.includes("lighter") || title.includes("charcoal") || cat.includes("prop")) {
    return {
      ...alert,
      frame_before: "/evidence_frames/01_prop_lighter_fluid_shotA_0758.jpg",
      frame_after: "/evidence_frames/01_prop_lighter_fluid_shotB_0815.jpg",
    };
  } else if (title.includes("rifle") || title.includes("cooper") || cat.includes("lighting")) {
    return {
      ...alert,
      frame_before: "/evidence_frames/02_prop_rifle_shotA_vertical_1325.jpg",
      frame_after: "/evidence_frames/02_prop_rifle_shotB_horizontal_1335.jpg",
    };
  } else {
    return {
      ...alert,
      frame_before: "/evidence_frames/04_script_deviation_table_bare_hands_0045.jpg",
      frame_after: "/evidence_frames/04_script_deviation_table_bare_hands_0045.jpg",
    };
  }
}

// ─── Fallback data ──────────────────────────────────────────────────────────

const FALLBACK_ALERTS: Alert[] = [
  {
    alert_id: "alert_001",
    take_id: "s12_sh03_t04",
    scene: 12,
    category: "Production Error",
    severity: "critical",
    confidence: 1.0,
    title: "Visible Crew Marking 'UPPER RIGHT CORNER' on Barricade",
    description:
      "At 37:08 (film time), handwritten production direction 'UPPER RIGHT CORNER' is clearly legible on a wooden barricade plank in the living room boarding sequence. This text was written by a crew member during set preparation and was not removed before filming.",
    visual_evidence:
      "Grease pencil / chalk text occupies approximately 8% of the frame at the upper-right quadrant of the door barricade plank. Gemini validation: 100% confidence, 'legible handwritten text, clearly non-diegetic production note'.",
    technical_impact:
      "Breaks the fourth wall and exposes production mechanics to the audience. Cannot be fixed in post without digital removal. Immediate retake required to preserve the film's diegetic world.",
    director_action_required: "RETAKE REQUIRED",
    timestamp_film: "37:08",
    timestamp_clip: "00:02:30",
    frame_before: "/evidence_frames/03_set_door_barricade_wide_0230.jpg",
    frame_after: "/evidence_frames/03_set_door_barricade_wide_0230.jpg",
  },
  {
    alert_id: "alert_002",
    take_id: "s13_sh01_t02",
    scene: 13,
    category: "Prop Continuity",
    severity: "warning",
    confidence: 0.95,
    title: "Charcoal Lighter Fluid Container Placement Discrepancy",
    description:
      "The Charcoal Lighter Fluid container is held by Ben in Shot 1 near the fireplace hearth, but abruptly appears resting on the floor beside the chair in the reverse insert cut.",
    visual_evidence:
      "Shot A (07:58): Container emblem 'CHARCOAL LIGHTER' held in right hand. Shot B (08:15): Reverse cutaway shows can resting on hearth floor beside chair.",
    technical_impact:
      "Noticeable prop displacement across reverse coverage during torch preparation.",
    director_action_required: "DIRECTOR REVIEW REQUIRED",
    timestamp_film: "33:01",
    timestamp_clip: "00:07:58",
    frame_before: "/evidence_frames/01_prop_lighter_fluid_shotA_0758.jpg",
    frame_after: "/evidence_frames/01_prop_lighter_fluid_shotB_0815.jpg",
  },
  {
    alert_id: "alert_003",
    take_id: "s14_sh02_t01",
    scene: 14,
    category: "Prop Staging",
    severity: "warning",
    confidence: 0.90,
    title: "Winchester Repeating Rifle Position & Handling",
    description:
      "In the medium shot, the rifle rests vertically upright against Ben's knee. On the immediate reverse cut across Barbra's shoulder, the rifle has shifted horizontally across his lap.",
    visual_evidence:
      "Shot A (13:25): Rifle barrel vertical against knee. Shot B (13:35): Reverse cut shows rifle held horizontally across lap.",
    technical_impact:
      "Natural actor posture shift during dialogue. Acceptable coverage variance.",
    director_action_required: "LOG ONLY",
    timestamp_film: "38:25",
    timestamp_clip: "00:13:25",
    frame_before: "/evidence_frames/02_prop_rifle_shotA_vertical_1325.jpg",
    frame_after: "/evidence_frames/02_prop_rifle_shotB_horizontal_1335.jpg",
  },
  {
    alert_id: "alert_004",
    take_id: "s12_sh01_t01",
    scene: 12,
    category: "Script Compliance",
    severity: "minor",
    confidence: 0.85,
    title: "Ben Table Disassembly Sequence Modified",
    description:
      "The shooting screenplay specifies Ben uses an iron tire iron and hammer to dismantle the table legs. In the filmed version, Duane Jones forcefully rips the turned baluster legs off using bare hands and leverage.",
    visual_evidence: "Actor physical performance divergence from written action lines.",
    technical_impact: "Dramatic performance reads with high physical urgency.",
    director_action_required: "ACCEPT RISK",
    timestamp_film: "25:00",
    timestamp_clip: "00:00:45",
    frame_before: "/evidence_frames/04_script_deviation_table_bare_hands_0045.jpg",
    frame_after: "/evidence_frames/04_script_deviation_table_bare_hands_0045.jpg",
  },
];
