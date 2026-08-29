"""
Shadow Cut MCP Server — Tool 4: flag_alert
Implements the Decision Matrix from confidence_escalation_logic.md v2.0 (LOCKED).

Decision Matrix (Section 6 of the spec):
─────────────────────────────────────────────────────────────────────
  TechnicalConfidence   CRITICAL prop      IMPORTANT prop   INCIDENTAL
  High  (> 0.75)        ALERT (Instant)    ALERT (Std)      SILENT_LOG
  Med   (0.50–0.75)     ESCALATE → Pro     SILENT_LOG       SILENT_LOG
  Low   (< 0.50)        SILENT_LOG         SILENT_LOG       SUPPRESS
─────────────────────────────────────────────────────────────────────

Hard rules (Section 6 of the spec):
  1. Below 0.50 TechnicalConfidence → NEVER alert.
  2. CRITICAL + High confidence → ALWAYS alert (safety override).
  3. INCIDENTAL → NEVER alert regardless of confidence.
  4. Performance/emotion analysis → NEVER alert above MEDIUM
     unless director opted in (not tracked in this tool).
"""
from __future__ import annotations

from typing import Literal

from shadow_cut.models.schemas import (
    AlertActionLiteral,
    AlertDecision,
    Anomaly,
)


def tool(func):  # type: ignore[no-untyped-def]
    return func


# ---------------------------------------------------------------------------
# Decision Matrix — exactly as spec Section 6
# ---------------------------------------------------------------------------

def _apply_decision_matrix(
    confidence: float,
    plot_weight: Literal["CRITICAL", "IMPORTANT", "INCIDENTAL"],
) -> AlertActionLiteral:
    """
    Pure function implementing the locked Decision Matrix.
    Returns one of: ALERT | SILENT_LOG | SUPPRESS | ESCALATE
    """
    # Hard rule 3: INCIDENTAL → NEVER alert
    if plot_weight == "INCIDENTAL":
        return "SILENT_LOG"

    # High confidence band (> 0.75)
    if confidence > 0.75:
        # Hard rule 2: CRITICAL + High → ALWAYS alert
        return "ALERT"  # covers both CRITICAL (instant) and IMPORTANT (standard)

    # Medium confidence band (0.50 – 0.75)
    if confidence >= 0.50:
        if plot_weight == "CRITICAL":
            return "ESCALATE"
        return "SILENT_LOG"

    # Low confidence band (< 0.50)
    # Hard rule 1: below 0.50 → NEVER alert
    if plot_weight == "INCIDENTAL":
        return "SUPPRESS"
    return "SILENT_LOG"


# ---------------------------------------------------------------------------
# Escalation logic — Section 7 of the spec
# ---------------------------------------------------------------------------

def _should_escalate_to_pro(
    anomaly: Anomaly,
    confidence: float,
    plot_weight: Literal["CRITICAL", "IMPORTANT", "INCIDENTAL"],
    pro_budget_remaining: int,
) -> tuple[bool, str | None]:
    """
    Decide whether to escalate to Gemini Pro.
    Budget guard is evaluated FIRST (was dead-code in the broken v1).
    Returns (should_escalate, reason_or_None).
    """
    # Budget guard — FIRST (Section 7, step 1)
    if pro_budget_remaining <= 0 and plot_weight != "CRITICAL":
        return False, None  # CRITICAL still bypasses budget

    # Hard skip rules (Section 7, step 2)
    if confidence >= 0.90:
        return False, None  # already certain
    if plot_weight == "INCIDENTAL":
        return False, None  # never escalate background clutter

    # Auto-escalate triggers (Section 7, step 3)
    if plot_weight == "CRITICAL" and confidence < 0.85:
        return True, "CRITICAL prop below 0.85 confidence — Pro verification required"
    if anomaly.is_cross_scene:
        return True, "Cross-scene continuity — non-linear reasoning required"
    if anomaly.is_novel and plot_weight in ("CRITICAL", "IMPORTANT"):
        return True, "Novel anomaly type on important prop — Pro review required"
    if anomaly.evidence_source_count < 2 and plot_weight == "CRITICAL":
        return True, "Single-source CRITICAL claim needs corroboration"

    return False, None


# ---------------------------------------------------------------------------
# Reasoning builder
# ---------------------------------------------------------------------------

def _build_reasoning(
    confidence: float,
    plot_weight: str,
    action: AlertActionLiteral,
    anomaly: Anomaly,
) -> str:
    band = (
        "High (> 0.75)" if confidence > 0.75
        else "Medium (0.50–0.75)" if confidence >= 0.50
        else "Low (< 0.50)"
    )
    return (
        f"TechnicalConfidence={confidence:.3f} [{band}], "
        f"PlotWeight={plot_weight} → Action={action}. "
        f"Prop: {anomaly.prop_name or 'N/A'}, "
        f"Scene: {anomaly.scene}, "
        f"Category: {anomaly.category}."
    )


# ---------------------------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------------------------

@tool
def flag_alert(
    anomaly: Anomaly,
    confidence: float,
    plot_weight: Literal["CRITICAL", "IMPORTANT", "INCIDENTAL"],
    pro_budget_remaining: int = 50,
) -> AlertDecision:
    """
    Apply the Shadow Cut Decision Matrix to an anomaly and return the action to take.

    Implements the locked v2.0 Decision Matrix from confidence_escalation_logic.md:
      - PlotWeight is a GATE, not a multiplier.
      - Budget guard runs FIRST inside the escalation check.
      - INCIDENTAL props are always SILENT_LOG, never alerted.
      - Below 0.50 confidence → SILENT_LOG (SUPPRESS only for INCIDENTAL < 0.50).

    Args:
        anomaly:               Structured anomaly description.
        confidence:            Pre-calculated TechnicalConfidence (0.0–1.0).
                               Formula: EvidenceQuality × HistoricalAccuracy × DirectorTrust.
        plot_weight:           Script-derived importance gate: CRITICAL | IMPORTANT | INCIDENTAL.
        pro_budget_remaining:  How many Pro escalations remain today (default 50).

    Returns:
        AlertDecision with action, reasoning, and escalation recommendation.
    """
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"confidence must be in [0, 1], got {confidence}")

    action = _apply_decision_matrix(confidence, plot_weight)

    # Resolve ESCALATE action via escalation logic
    should_esc, esc_reason = _should_escalate_to_pro(
        anomaly, confidence, plot_weight, pro_budget_remaining
    )

    # If the matrix said ESCALATE but the escalation logic says no (e.g. budget),
    # degrade to SILENT_LOG
    if action == "ESCALATE" and not should_esc:
        action = "SILENT_LOG"
        esc_reason = None

    reasoning = _build_reasoning(confidence, plot_weight, action, anomaly)

    return AlertDecision(
        action=action,
        confidence=confidence,
        plot_weight=plot_weight,
        reasoning=reasoning,
        should_escalate_to_pro=should_esc,
        escalation_reason=esc_reason,
    )
