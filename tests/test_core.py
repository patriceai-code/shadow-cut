"""
Shadow Cut Core Test Suite
Validates:
1. Pydantic v2 Schema validation for Confluent / Webhook Ingress (TakePayload, TakeUploadedEvent)
2. Confidence & Escalation Engine Decision Matrix (Director Autonomy Principle)
3. MCP Server Tool Decision Matrix (flag_alert)
4. Bounding box and Alert contract invariants
"""

import pytest
from pydantic import ValidationError

from shadow_cut.stream.confluent_consumer import TakePayload, TakeUploadedEvent
from shadow_cut.core.confidence import ConfidenceEngine, PlotWeight, Action, Anomaly, EvidenceSource
from shadow_cut.mcp_servers.flag_alert import _apply_decision_matrix
from shadow_cut.models.schemas import BoundingBox
from shadow_cut.models.data_models import DirectorAlert


class TestTakeIngressValidation:
    """Test Pydantic v2 schemas for take ingestion."""

    def test_valid_take_payload(self):
        payload = TakePayload(
            take_id="s12_sh01_t04",
            video_path="/data/takes/s12_sh01_t04.mp4",
            scene=12,
            shot=1,
            take=4,
            duration=45.2,
            production_id="notld-1968"
        )
        assert payload.take_id == "s12_sh01_t04"
        assert payload.scene == 12
        assert payload.duration == 45.2

    def test_invalid_take_id_pattern(self):
        with pytest.raises(ValidationError):
            # Take ID must match pattern ^s[0-9]+_sh[0-9]+_t[0-9]+$
            TakePayload(
                take_id="invalid_take_format",
                video_path="/data/takes/test.mp4",
                scene=1,
                shot=1,
                take=1
            )

    def test_valid_event_envelope(self):
        event = TakeUploadedEvent(
            event_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            timestamp="2026-09-04T12:00:00Z",
            type="take_uploaded",
            data=TakePayload(
                take_id="s01_sh01_t01",
                video_path="/data/takes/s01_sh01_t01.mp4",
                scene=1,
                shot=1,
                take=1
            )
        )
        assert event.data.take_id == "s01_sh01_t01"
        assert event.type == "take_uploaded"


class TestDirectorAutonomyAndConfidence:
    """Test the Director Autonomy Principle and ConfidenceEngine."""

    @pytest.fixture
    def engine(self):
        return ConfidenceEngine(pro_budget=50)

    def test_critical_prop_high_confidence_instant_alert(self, engine):
        anomaly = Anomaly(category="prop_displacement", prop_name="lighter_fluid", scene=7)
        action = engine.decide_action(anomaly, tech_confidence=0.88, plot_weight=PlotWeight.CRITICAL)
        assert action == Action.ALERT_INSTANT

    def test_critical_prop_medium_confidence_escalates_to_pro(self, engine):
        anomaly = Anomaly(category="prop_state", prop_name="winchester_rifle", scene=52)
        action = engine.decide_action(anomaly, tech_confidence=0.65, plot_weight=PlotWeight.CRITICAL)
        assert action == Action.ESCALATE_TO_PRO

    def test_incidental_prop_always_silent_log(self, engine):
        # Director Autonomy: Never interrupt director for incidental background items
        anomaly = Anomaly(category="background_prop", prop_name="curtain_crease", scene=18)
        action = engine.decide_action(anomaly, tech_confidence=0.95, plot_weight=PlotWeight.INCIDENTAL)
        assert action == Action.SILENT_LOG

    def test_multi_source_evidence_boost(self, engine):
        single_source = Anomaly(
            category="prop_displacement",
            prop_name="chair",
            scene=12,
            evidence_sources=[EvidenceSource("yolo_world", 0.70, "Bounding box shift")]
        )
        multi_source = Anomaly(
            category="prop_displacement",
            prop_name="chair",
            scene=12,
            evidence_sources=[
                EvidenceSource("yolo_world", 0.70, "Bounding box shift"),
                EvidenceSource("flash_lite", 0.85, "Visual verification")
            ]
        )
        single_conf = engine.calculate_technical_confidence(single_source)
        multi_conf = engine.calculate_technical_confidence(multi_source)
        assert multi_conf > single_conf


class TestMCPFlagAlertMatrix:
    """Test Tool 4: flag_alert pure decision matrix."""

    def test_mcp_decision_matrix_rules(self):
        # Rule 1: High confidence + CRITICAL -> ALERT
        assert _apply_decision_matrix(0.85, "CRITICAL") == "ALERT"
        # Rule 2: High confidence + IMPORTANT -> ALERT
        assert _apply_decision_matrix(0.80, "IMPORTANT") == "ALERT"
        # Rule 3: High confidence + INCIDENTAL -> SILENT_LOG
        assert _apply_decision_matrix(0.95, "INCIDENTAL") == "SILENT_LOG"
        # Rule 4: Medium confidence + CRITICAL -> ESCALATE
        assert _apply_decision_matrix(0.60, "CRITICAL") == "ESCALATE"
        # Rule 5: Medium confidence + IMPORTANT -> SILENT_LOG
        assert _apply_decision_matrix(0.60, "IMPORTANT") == "SILENT_LOG"
        # Rule 6: Low confidence (<0.50) + CRITICAL -> SILENT_LOG
        assert _apply_decision_matrix(0.40, "CRITICAL") == "SILENT_LOG"
        # Rule 7: Low confidence + INCIDENTAL -> SILENT_LOG (suppresses interruption)
        assert _apply_decision_matrix(0.30, "INCIDENTAL") == "SILENT_LOG"


class TestModelSchemas:
    """Test bounding box geometric integrity constraints."""

    def test_valid_bounding_box(self):
        bbox = BoundingBox(
            x1=100,
            y1=150,
            x2=450,
            y2=600
        )
        assert bbox.x1 == 100
        assert bbox.x2 == 450
        assert bbox.y2 > bbox.y1

    def test_invalid_bounding_box_inverted_coords(self):
        with pytest.raises(ValidationError):
            # x2 must be strictly greater than x1
            BoundingBox(
                x1=500,
                y1=150,
                x2=200,
                y2=600
            )
