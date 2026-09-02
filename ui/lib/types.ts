// ─── Shadow Cut shared domain types ───────────────────────────────────────

export interface Alert {
  alert_id: string;
  take_id: string;
  scene: number;
  category: string;
  severity: "critical" | "warning" | "info" | "minor";
  confidence: number;
  title: string;
  description: string;
  visual_evidence?: string;
  technical_impact?: string;
  director_action_required?: "RETAKE REQUIRED" | "DIRECTOR REVIEW REQUIRED" | "LOGGED" | "LOG ONLY" | "ACCEPT RISK";
  timestamp_film?: string;
  timestamp_clip?: string;
  frame_before?: string; // base64 or URL
  frame_after?: string;  // base64 or URL
}

export interface ScriptDeviation {
  timestamp_film: string;
  scripted_element: string;
  filmed_reality: string;
  severity: "critical" | "warning" | "info" | "minor";
  objective_impact: string;
  character?: string;
  scene_number?: number;
}

export interface DashboardStats {
  cuts_analyzed: number;
  retake_required: number;
  director_review: number;
  script_compliance: number;
  production_title: string;
  scene_range: string;
  timecode_range: string;
}

export interface ChatMessage {
  role: "director" | "assistant";
  text: string;
  timestamp?: string;
}

export interface TrustReport {
  production_title: string;
  scene_range: string;
  reshoot_savings_usd: number;
  compute_cost_usd: number;
  director_autonomy_pct: number;
  cuts_analyzed: number;
  retakes_caught: number;
  accuracy_pct: number;
  executive_verdict: string;
  date: string;
}

export type DirectorDecision = "retake" | "accept" | "dismiss";
export type ActiveTab = "dashboard" | "alerts" | "deviations" | "chat" | "report";
