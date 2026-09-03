# mcp_servers/flag_alert.py
"""
Flag alert tool for Shadow Cut.
If using IBM Bob / watsonx Orchestrate, Bob will generate the @tool decorator.
For local development and testing, defined as a plain typed function.
"""
from shadow_cut.core.confidence import ConfidenceEngine, Anomaly, PlotWeight

def flag_alert(anomaly: dict, confidence: float, plot_weight: str) -> dict:
    """Use Decision Matrix to determine ALERT / SILENT_LOG / SUPPRESS."""
    engine = ConfidenceEngine()
    anom_obj = Anomaly(
        category=anomaly.get("category", anomaly.get("type", "unknown")),
        prop_name=anomaly.get("prop"),
        scene=anomaly.get("scene", 1),
        is_cross_scene=anomaly.get("is_cross_scene", False),
        is_novel=anomaly.get("is_novel", False)
    )
    weight = PlotWeight.CRITICAL if plot_weight == "CRITICAL" else (
        PlotWeight.IMPORTANT if plot_weight == "IMPORTANT" else PlotWeight.INCIDENTAL
    )
    action = engine.decide_action(anom_obj, confidence, weight)
    return {
        "action": action.value,
        "confidence": confidence,
        "plot_weight": plot_weight,
        "reasoning": f"Evaluated with confidence {confidence:.2f} and {plot_weight} priority."
    }
