"""
Shadow Cut MCP Server — Tool 3: check_continuity
Compares prop states across takes and against script rules in the PlotKnowledgeGraph.
"""
from __future__ import annotations

from shadow_cut.models.schemas import (
    ContinuityMatch,
    ContinuityMismatch,
    ContinuityReport,
    CrossSceneIssue,
    PlotKnowledgeGraph,
    PropStateSnapshot,
    Take,
)


def tool(func):  # type: ignore[no-untyped-def]
    return func


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _plot_weight_for_prop(prop_name: str, graph: PlotKnowledgeGraph) -> str:
    """Look up PlotWeight from graph; default to INCIDENTAL if not found."""
    for prop in graph.props:
        if prop.canonical_name.lower() == prop_name.lower():
            return prop.plot_weight
    return "INCIDENTAL"


def _severity_from_weight(weight: str) -> str:
    return {"CRITICAL": "critical", "IMPORTANT": "warning", "INCIDENTAL": "info"}.get(weight, "info")


def _rule_for_prop(prop_name: str, graph: PlotKnowledgeGraph) -> str | None:
    """Return the first continuity rule for a prop, if any."""
    for prop in graph.props:
        if prop.canonical_name.lower() == prop_name.lower() and prop.continuity_rules:
            return prop.continuity_rules[0]
    return None


def _expected_state(prop_name: str, scene_number: int, graph: PlotKnowledgeGraph) -> str | None:
    """
    Find the expected state for a prop in a given scene from the plot graph.
    Returns None if not specified.
    """
    for scene in graph.scenes:
        if scene.number == scene_number:
            for sp in scene.critical_props + scene.important_props:
                if sp.prop_name.lower() == prop_name.lower():
                    return sp.scene_state
    return None


def _index_by_prop(snapshots: list[PropStateSnapshot]) -> dict[str, PropStateSnapshot]:
    return {s.prop_name.lower(): s for s in snapshots}


# ---------------------------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------------------------

@tool
def check_continuity(
    current_take: Take,
    previous_takes: list[Take],
    plot_graph: PlotKnowledgeGraph,
) -> ContinuityReport:
    """
    Compare a take's prop states against previous takes and script rules.

    Three checks are performed:
    1. **Prop-to-prop**: compare each prop state in `current_take` against the
       most recent previous take that observed the same prop.
    2. **Script-rule**: compare current prop states against the expected state
       defined for this scene in the PlotKnowledgeGraph.
    3. **Cross-scene**: flag any prop whose scene transitions violate the
       setup/payoff links in the graph (e.g., payoff prop seen before setup scene).

    Args:
        current_take:   The take just analysed.
        previous_takes: All prior takes for this production (newest first preferred).
        plot_graph:     Validated PlotKnowledgeGraph for the production.

    Returns:
        ContinuityReport with matches, mismatches, and cross-scene issues.
    """
    matches: list[ContinuityMatch] = []
    mismatches: list[ContinuityMismatch] = []
    cross_issues: list[CrossSceneIssue] = []
    checked_props: set[str] = set()

    current_index = _index_by_prop(current_take.prop_states)

    # ── 1. Prop-to-prop comparison ─────────────────────────────────────────
    # Walk previous takes from most-recent to oldest; use first match per prop.
    seen_in_prev: dict[str, tuple[PropStateSnapshot, str]] = {}
    for prev in previous_takes:
        for snap in prev.prop_states:
            key = snap.prop_name.lower()
            if key not in seen_in_prev:
                seen_in_prev[key] = (snap, prev.take_id)

    for prop_key, cur_snap in current_index.items():
        checked_props.add(prop_key)
        weight = _plot_weight_for_prop(prop_key, plot_graph)

        if prop_key in seen_in_prev:
            prev_snap, prev_take_id = seen_in_prev[prop_key]
            if cur_snap.observed_state == prev_snap.observed_state:
                matches.append(
                    ContinuityMatch(
                        prop_name=cur_snap.prop_name,
                        current_take_id=current_take.take_id,
                        previous_take_id=prev_take_id,
                        state=cur_snap.observed_state,
                        confidence=min(cur_snap.confidence, prev_snap.confidence),
                    )
                )
            else:
                rule = _rule_for_prop(prop_key, plot_graph)
                mismatches.append(
                    ContinuityMismatch(
                        prop_name=cur_snap.prop_name,
                        current_state=cur_snap.observed_state,
                        expected_state=prev_snap.observed_state,
                        current_take_id=current_take.take_id,
                        previous_take_id=prev_take_id,
                        plot_weight=weight,  # type: ignore[arg-type]
                        severity=_severity_from_weight(weight),  # type: ignore[arg-type]
                        rule_violated=rule,
                    )
                )

    # ── 2. Script-rule check ───────────────────────────────────────────────
    for prop_key, cur_snap in current_index.items():
        expected = _expected_state(prop_key, current_take.scene, plot_graph)
        if expected is None:
            continue
        if cur_snap.observed_state != expected:
            weight = _plot_weight_for_prop(prop_key, plot_graph)
            rule = _rule_for_prop(prop_key, plot_graph)
            # Avoid duplicating a mismatch already caught above
            already_flagged = any(
                m.prop_name.lower() == prop_key for m in mismatches
            )
            if not already_flagged:
                mismatches.append(
                    ContinuityMismatch(
                        prop_name=cur_snap.prop_name,
                        current_state=cur_snap.observed_state,
                        expected_state=expected,
                        current_take_id=current_take.take_id,
                        previous_take_id="script",
                        plot_weight=weight,  # type: ignore[arg-type]
                        severity=_severity_from_weight(weight),  # type: ignore[arg-type]
                        rule_violated=rule,
                    )
                )

    # ── 3. Cross-scene setup/payoff checks ────────────────────────────────
    for link in plot_graph.setups:
        if link.prop_involved is None:
            continue
        prop_key = link.prop_involved.lower()
        if prop_key not in current_index:
            continue
        # Payoff prop observed before its setup scene
        if current_take.scene < link.setup_scene:
            cross_issues.append(
                CrossSceneIssue(
                    description=(
                        f"Prop '{link.prop_involved}' observed in scene {current_take.scene} "
                        f"but setup is not until scene {link.setup_scene}."
                    ),
                    scenes_involved=[current_take.scene, link.setup_scene],
                    prop_name=link.prop_involved,
                    severity="warning",
                )
            )
        # Payoff prop still in setup-state after its payoff scene
        if current_take.scene > link.payoff_scene and link.status == "open":
            cross_issues.append(
                CrossSceneIssue(
                    description=(
                        f"Setup '{link.description}' is unresolved past payoff "
                        f"scene {link.payoff_scene} (current scene {current_take.scene})."
                    ),
                    scenes_involved=[link.setup_scene, link.payoff_scene, current_take.scene],
                    prop_name=link.prop_involved,
                    severity="critical",
                )
            )

    return ContinuityReport(
        current_take_id=current_take.take_id,
        matches=matches,
        mismatches=mismatches,
        cross_scene_issues=cross_issues,
        total_props_checked=len(checked_props),
    )
