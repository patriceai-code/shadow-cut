"""
Confidence & Escalation Engine v2.0 (Patched)
- PlotWeight is a GATE (Decision Matrix), not a multiplier
- Budget guard at TOP of function (was dead code before)
- Cold-start HistoricalAccuracy = 0.95
"""
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field

class PlotWeight(Enum):
    CRITICAL = "CRITICAL"
    IMPORTANT = "IMPORTANT"
    INCIDENTAL = "INCIDENTAL"

class Action(Enum):
    ALERT_INSTANT = "alert_instant"
    ALERT_STANDARD = "alert_standard"
    ESCALATE_TO_PRO = "escalate_to_pro"
    SILENT_LOG = "silent_log"
    SUPPRESS = "suppress"

@dataclass
class EvidenceSource:
    source_type: str
    reliability: float
    description: str

@dataclass
class Anomaly:
    category: str
    prop_name: Optional[str]
    scene: int
    is_cross_scene: bool = False
    is_novel: bool = False
    evidence_sources: List[EvidenceSource] = field(default_factory=list)

class ConfidenceEngine:
    def __init__(self, pro_budget: int = 50):
        self.pro_escalation_count_today = 0
        self.pro_budget = pro_budget
        self.dismissal_tracker = {}
        self.accuracy_tracker = {}

    def calculate_technical_confidence(self, anomaly: Anomaly) -> float:
        if not anomaly.evidence_sources:
            evidence_score = 0.40
        else:
            scores = [s.reliability for s in anomaly.evidence_sources]
            evidence_score = max(scores)
            if len(scores) >= 2:
                evidence_score = min(evidence_score + 0.08, 0.98)

        category = anomaly.category
        if category in self.accuracy_tracker:
            hits, misses = self.accuracy_tracker[category]
            total = hits + misses
            if total > 0:
                hist_acc = hits / total
                if hist_acc > 0.90: hist_acc = 1.00
                elif hist_acc > 0.75: hist_acc = 0.95
                elif hist_acc > 0.50: hist_acc = 0.90
                else: hist_acc = 0.60
            else:
                hist_acc = 0.95
        else:
            hist_acc = 0.95

        dismissals = self.dismissal_tracker.get(category, 0)
        if dismissals >= 3: director_trust = 0.50
        elif dismissals == 2: director_trust = 0.75
        elif dismissals == 1: director_trust = 0.90
        else: director_trust = 1.00

        confidence = evidence_score * hist_acc * director_trust
        return min(confidence, 0.99)

    def decide_action(self, anomaly: Anomaly, tech_confidence: float, plot_weight: PlotWeight) -> Action:
        if plot_weight == PlotWeight.INCIDENTAL:
            return Action.SILENT_LOG
        if tech_confidence > 0.75:
            if plot_weight == PlotWeight.CRITICAL:
                return Action.ALERT_INSTANT
            else:
                return Action.ALERT_STANDARD
        elif tech_confidence >= 0.50:
            if plot_weight == PlotWeight.CRITICAL:
                return Action.ESCALATE_TO_PRO
            else:
                return Action.SILENT_LOG
        else:
            return Action.SILENT_LOG

    def should_escalate_to_pro(self, anomaly: Anomaly, tech_confidence: float, plot_weight: PlotWeight) -> bool:
        if self.pro_escalation_count_today >= self.pro_budget:
            if plot_weight != PlotWeight.CRITICAL:
                return False
        if tech_confidence >= 0.90:
            return False
        if plot_weight == PlotWeight.INCIDENTAL:
            return False
        if plot_weight == PlotWeight.CRITICAL and tech_confidence < 0.85:
            return True
        if anomaly.is_cross_scene:
            return True
        if anomaly.is_novel and plot_weight in [PlotWeight.CRITICAL, PlotWeight.IMPORTANT]:
            return True
        return False

    def record_outcome(self, category: str, director_action: str):
        if category not in self.accuracy_tracker:
            self.accuracy_tracker[category] = [0, 0]
        if director_action == "confirm":
            self.accuracy_tracker[category][0] += 1
        elif director_action == "dismiss":
            self.accuracy_tracker[category][1] += 1
            self.dismissal_tracker[category] = self.dismissal_tracker.get(category, 0) + 1
        elif director_action == "dismiss_forever":
            self.accuracy_tracker[category][1] += 1
            self.dismissal_tracker[category] = self.dismissal_tracker.get(category, 0) + 3
