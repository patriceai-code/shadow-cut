"""
Shadow Cut MCP Server — Tool 6: generate_report
Aggregates Shadow Memory for a date range and produces a typed DailyReport.
"""
from __future__ import annotations

from shadow_cut.config.settings import get_settings
from shadow_cut.models.schemas import CostBreakdown, DailyReport, TakeAccuracyRow


def tool(func):  # type: ignore[no-untyped-def]
    return func


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def _aggregate_firestore(
    date_from: str,
    date_to: str,
    production_id: str,
    settings,  # type: ignore[no-untyped-def]
) -> dict:
    """
    Pull takes and alerts from Firestore for the given date window.

    Returns a raw aggregation dict with counts and per-scene rows.
    Falls back to zeroed structure if Firestore is unreachable.
    """
    from google.cloud import firestore  # type: ignore[import-untyped]

    db = firestore.Client(project=settings.firestore_project_id)

    takes_analyzed = 0
    alerts_generated = 0
    confirmed = 0
    false_positives = 0
    flash_lite_calls = 0
    pro_escalations = 0
    flash_cost = 0.0
    pro_cost = 0.0
    scene_rows: dict[int, dict] = {}
    alert_categories: list[str] = []

    try:
        takes_ref = (
            db.collection("takes")
            .where("production_id", "==", production_id)
            .where("date", ">=", date_from)
            .where("date", "<=", date_to)
        )
        for doc in takes_ref.get():
            data: dict = doc.to_dict() or {}
            takes_analyzed += 1
            scene = int(data.get("scene", 0))
            cost: float = float(data.get("cost_usd", 0.002))
            flash_cost += cost
            flash_lite_calls += 1

            if scene not in scene_rows:
                scene_rows[scene] = {
                    "takes": 0, "alerts": 0, "confirmed": 0, "fp": 0
                }
            scene_rows[scene]["takes"] += 1
    except Exception:
        pass

    try:
        alerts_ref = (
            db.collection("alerts")
            .where("production_id", "==", production_id)
            .where("date", ">=", date_from)
            .where("date", "<=", date_to)
        )
        for doc in alerts_ref.get():
            data = doc.to_dict() or {}
            alerts_generated += 1
            scene = int(data.get("scene", 0))
            action = str(data.get("director_action", ""))
            category = str(data.get("category", "unknown"))
            if category not in alert_categories:
                alert_categories.append(category)

            if action == "confirm":
                confirmed += 1
                if scene in scene_rows:
                    scene_rows[scene]["confirmed"] += 1
            elif action in ("dismiss", "dismiss_forever"):
                false_positives += 1
                if scene in scene_rows:
                    scene_rows[scene]["fp"] += 1

            if data.get("escalated_to_pro"):
                pro_escalations += 1
                pro_cost += float(data.get("pro_cost_usd", 0.010))

            if scene in scene_rows:
                scene_rows[scene]["alerts"] += 1
    except Exception:
        pass

    return {
        "takes_analyzed": takes_analyzed,
        "alerts_generated": alerts_generated,
        "confirmed": confirmed,
        "false_positives": false_positives,
        "flash_lite_calls": flash_lite_calls,
        "pro_escalations": pro_escalations,
        "flash_cost": flash_cost,
        "pro_cost": pro_cost,
        "scene_rows": scene_rows,
        "alert_categories": alert_categories,
    }


def _calculate_accuracy(confirmed: int, false_positives: int) -> float:
    total = confirmed + false_positives
    if total == 0:
        return 1.0
    return round(confirmed / total, 4)


def _savings_estimate(confirmed_alerts: int) -> float:
    """
    Conservative savings estimate.
    Each confirmed alert prevented an average reshooting cost of $15 000.
    (Industry estimate: $15 k–$80 k per continuity reshoot day.)
    """
    return float(confirmed_alerts * 15_000)


# ---------------------------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------------------------

@tool
def generate_report(
    date_range: tuple[str, str],
    production_id: str,
) -> DailyReport:
    """
    Generate a DailyReport (Trust Report) for a production and date window.

    Aggregates take analysis results and director-confirmed alerts from Shadow
    Memory (Firestore), calculates accuracy metrics, cost breakdown, and a
    savings estimate based on confirmed continuity catches.

    Args:
        date_range:     ISO-8601 date strings (from, to) inclusive, e.g.
                        ("2026-08-01", "2026-08-01").
        production_id:  Production identifier (e.g. "shadow-cut-hackathon").

    Returns:
        DailyReport with takes_analyzed, alerts_generated, accuracy, cost,
        savings_estimate, scene breakdown, and top alert categories.
    """
    if len(date_range) != 2:
        raise ValueError("date_range must be a (from, to) tuple of ISO date strings")

    date_from, date_to = date_range
    if date_from > date_to:
        raise ValueError("date_range[0] must be <= date_range[1]")

    settings = get_settings()
    agg = _aggregate_firestore(date_from, date_to, production_id, settings)

    accuracy = _calculate_accuracy(agg["confirmed"], agg["false_positives"])
    total_cost = agg["flash_cost"] + agg["pro_cost"]

    cost = CostBreakdown(
        flash_lite_calls=agg["flash_lite_calls"],
        pro_escalations=agg["pro_escalations"],
        flash_lite_cost_usd=round(agg["flash_cost"], 6),
        pro_cost_usd=round(agg["pro_cost"], 6),
        total_cost_usd=round(total_cost, 6),
    )

    scene_breakdown: list[TakeAccuracyRow] = []
    for scene_num, row in sorted(agg["scene_rows"].items()):
        if scene_num < 1:
            continue
        total_scene = row["confirmed"] + row["fp"]
        scene_acc = round(row["confirmed"] / total_scene, 4) if total_scene > 0 else 1.0
        scene_breakdown.append(
            TakeAccuracyRow(
                scene=scene_num,
                takes_analyzed=row["takes"],
                alerts_generated=row["alerts"],
                confirmed_alerts=row["confirmed"],
                false_positives=row["fp"],
                accuracy=scene_acc,
            )
        )

    return DailyReport(
        production_id=production_id,
        date_from=date_from,
        date_to=date_to,
        takes_analyzed=agg["takes_analyzed"],
        alerts_generated=agg["alerts_generated"],
        confirmed_alerts=agg["confirmed"],
        false_positives=agg["false_positives"],
        accuracy=accuracy,
        cost=cost,
        savings_estimate_usd=_savings_estimate(agg["confirmed"]),
        scene_breakdown=scene_breakdown,
        top_alert_categories=agg["alert_categories"][:10],
        notes=f"Report generated for production '{production_id}', {date_from} – {date_to}.",
    )
