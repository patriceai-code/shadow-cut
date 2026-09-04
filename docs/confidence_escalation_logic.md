# Shadow Cut — Confidence & Escalation Logic
## Deliverable 4: Algorithmic Ruleset (Zero-Laptop)
### Status: LOCKED v2.0 — Bugs patched per external review

---

## 1. THE CONFIDENCE FORMULA (FIXED)

**OLD (BROKEN):** `ShadowConfidence = EvidenceQuality × PlotWeight × HistoricalAccuracy × DirectorTrust`
**Problem:** Multiplying four decimals crushes legitimate alerts below 0.70. Even CRITICAL props with good evidence score ~0.58.

**NEW:**
```
TechnicalConfidence = EvidenceQuality × HistoricalAccuracy × DirectorTrust
```

PlotWeight is **NOT a multiplier**. It is a **gate** that determines action severity via the decision matrix (Section 6).

**Cold-start HistoricalAccuracy raised to 0.95** so new categories aren't penalized until they actually fail.

---

## 2. EVIDENCE QUALITY (Base Reliability)

| Source | Reliability | Rationale |
|--------|-------------|-----------|
| Script supervisor note (human-verified) | 0.95 | Human on set, directly observed |
| Slate metadata (objective) | 0.92 | Camera-generated, tamper-resistant |
| YOLO detection (multiple frames agree) | 0.85 | CV-verifiable, bounding boxes inspectable |
| YOLO detection (single frame only) | 0.65 | Possible false positive |
| Audio transcript (Gemini-native) | 0.75 | AI-transcribed, may miss jargon |
| Plot graph inference (script-based) | 0.65 | AI-inferred, no direct observation |
| Performance analysis (emotional tone) | 0.60 | Subjective interpretation |
| Gemini Flash-Lite validation | 0.70 | Model judgment, not raw sensor data |
| Gemini Pro escalation | 0.88 | Deeper reasoning, higher trust |

**Composite Evidence:**
- Two independent sources agree → boost by +0.08 (max 0.98)
- Sources conflict → drop to lowest source × 0.85
- No direct evidence (pure inference) → cap at 0.65

---

## 3. PLOT WEIGHT CLASSIFICATION (GATE, NOT MULTIPLIER)

| Classification | Definition |
|----------------|------------|
| **CRITICAL** | Setup/payoff prop, MacGuffin, character signature item |
| **IMPORTANT** | Supporting detail, recurring motif, thematic object |
| **INCIDENTAL** | Background clutter, set dressing, atmosphere |
| **UNKNOWN** | Not in script — possible improvisation or error |

**Rule:** INCIDENTAL props never trigger director alerts regardless of confidence. They are silently logged for chat queries only.

---

## 4. HISTORICAL ACCURACY (Self-Scoring)

Shadow tracks its own batting average per category:

```
HistoricalAccuracy = confirmed_alerts / (confirmed_alerts + false_positives)
```

| Accuracy Tier | Modifier | Example |
|---------------|----------|---------|
| Proven (>90%) | 1.00 | "Watch position" alerts — 12 sent, 11 confirmed |
| Reliable (75-90%) | 0.95 | "Letter state" alerts — 8 sent, 7 confirmed |
| Unproven (50-75%) | 0.90 | "Performance energy" alerts — new category |
| Unreliable (<50%) | 0.60 | "Lighting consistency" — 4 sent, 1 confirmed |

**Cold start:** New categories begin at **0.95** (optimistic but not arrogant).

---

## 5. DIRECTOR TRUST (Learning from Overrides)

If the director dismisses an alert category, Shadow adjusts:

```
DismissalCount = times director dismissed this category in last 7 days

if DismissalCount >= 3:
    DirectorTrust = 0.50      # Deprioritize heavily
    SeverityCap = "warning"   # Never show CRITICAL for this category
elif DismissalCount == 2:
    DirectorTrust = 0.75
elif DismissalCount == 1:
    DirectorTrust = 0.90
else:
    DirectorTrust = 1.00
```

**Override decay:** Dismissal counts decay by 1 every 48 hours.

**Explicit override types:**
- "Dismiss" → count +1
- "Dismiss & Don't Show Again" → count +3 (immediately triggers heavy deprioritization)
- "Confirm" → count -1 (minimum 0, rewards accurate alerts)

---

## 6. DECISION MATRIX (FIXED — PlotWeight as Gate)

TechnicalConfidence = EvidenceQuality × HistoricalAccuracy × DirectorTrust

| Tech Confidence | CRITICAL Prop | IMPORTANT Prop | INCIDENTAL Prop |
|-----------------|---------------|----------------|-----------------|
| **High (> 0.75)** | ALERT (Instant) | ALERT (Standard) | SILENT LOG |
| **Medium (0.50–0.75)** | ESCALATE TO PRO | SILENT LOG | SILENT LOG |
| **Low (< 0.50)** | SILENT LOG | SILENT LOG | SUPPRESS |

**Hard Rules:**
1. **Below 0.50 TechnicalConfidence → NEVER alert.** Only chat-queryable or suppressed.
2. **CRITICAL + High confidence → ALWAYS alert** (safety override).
3. **INCIDENTAL → NEVER alert** regardless of confidence.
4. **Performance/emotion analysis → NEVER alert above MEDIUM** unless director explicitly opts in.

---

## 7. ESCALATION MATRIX

When an anomaly is detected, the pipeline decides whether to escalate to Gemini Pro:

```
function should_escalate_to_pro(anomaly, technical_confidence, plot_weight):

    # 1. HARD CEILING: Budget guard FIRST (was dead code before)
    if pro_escalation_count_today >= pro_budget:
        if plot_weight != "CRITICAL":
            return false
        # CRITICAL props still allowed even over budget (safety override)

    # 2. Hard skip rules
    if technical_confidence >= 0.90:
        return false                         # Already certain
    if plot_weight == "INCIDENTAL":
        return false                         # Never escalate background clutter

    # 3. Auto-escalate triggers
    if plot_weight == "CRITICAL" and technical_confidence < 0.85:
        return true                          # Need Pro to verify critical prop
    if anomaly.is_cross_scene:
        return true                          # Non-linear continuity needs deep reasoning
    if anomaly.type == "performance_mismatch" and scene.importance == "climax":
        return true                          # High-stakes performance errors
    if anomaly.sources.count < 2 and plot_weight == "CRITICAL":
        return true                          # Single-source critical claim needs backup
    if anomaly.is_novel and plot_weight in ["CRITICAL", "IMPORTANT"]:
        return true                          # Never-seen-before issue on important prop

    # Default: let Flash-Lite handle it
    return false
```

**Escalation budget:** Max 15% of takes escalate to Pro. If budget exceeded, only CRITICAL props escalate (safety override).

---

## 8. ALERT DECISION TREE

```
ANOMALY DETECTED
    |
    v
+-----------------------------+
| Step 1: Calculate           |
| TechnicalConfidence =       |
| Evidence x History x Trust  |
+-----------------------------+
    |
    v
+-----------------------------+
| Step 2: Look up PlotWeight  |
| (CRITICAL/IMPORTANT/INC)    |
+-----------------------------+
    |
    v
+-----------------------------+
| Step 3: Apply Decision      |
| Matrix (Section 6)          |
| -> ALERT / LOG / ESCALATE   |
+-----------------------------+
    |
    v
+-----------------------------+
| Step 4: If ESCALATE, run    |
| should_escalate_to_pro()    |
| with budget guard FIRST     |
+-----------------------------+
    |
    v
+-----------------------------+
| Step 5: Final Action        |
| ALERT / SILENT_LOG / SUPPRESS|
+-----------------------------+
```

---

## 9. PSEUDOCODE (FIXED — Budget Guard at Top)

```python
class ConfidenceEngine:

    def __init__(self, shadow_memory):
        self.memory = shadow_memory
        self.dismissal_tracker = DismissalTracker(decay_hours=48)
        self.accuracy_tracker = AccuracyTracker()
        self.pro_escalation_count_today = 0
        self.pro_budget = 50  # max per day

    def calculate_technical_confidence(self, anomaly: Anomaly) -> float:
        # 1. Evidence quality
        evidence_score = self._score_evidence(anomaly.evidence_sources)

        # 2. Historical accuracy (cold start = 0.95)
        category = anomaly.category
        hist_acc = self.accuracy_tracker.get(category, default=0.95)

        # 3. Director trust
        director_trust = self.dismissal_tracker.get_trust(category)

        # Combine — PLOT WEIGHT IS NOT HERE
        confidence = evidence_score * hist_acc * director_trust
        return min(confidence, 0.99)

    def decide_action(self, anomaly: Anomaly, tech_confidence: float) -> Action:
        plot_weight = self._get_plot_weight(anomaly.prop_name, anomaly.scene)

        # Decision Matrix (Section 6)
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

        else:  # < 0.50
            return Action.SILENT_LOG

    def should_escalate_to_pro(self, anomaly: Anomaly, tech_confidence: float) -> bool:
        plot_weight = self._get_plot_weight(anomaly.prop_name, anomaly.scene)

        # FIX: Budget guard at TOP — prevents dead code
        if self.pro_escalation_count_today >= self.pro_budget:
            if plot_weight != PlotWeight.CRITICAL:
                return False
            # CRITICAL props bypass budget (safety override)

        # Hard skip rules
        if tech_confidence >= 0.90:
            return False
        if plot_weight == PlotWeight.INCIDENTAL:
            return False

        # Auto-escalate triggers
        if plot_weight == PlotWeight.CRITICAL and tech_confidence < 0.85:
            return True
        if anomaly.is_cross_scene:
            return True
        if anomaly.is_novel and plot_weight in [PlotWeight.CRITICAL, PlotWeight.IMPORTANT]:
            return True

        return False

    def record_outcome(self, alert_id: str, director_action: str):
        # Called after director responds to an alert
        if director_action == "confirm":
            self.accuracy_tracker.record_hit(alert_id)
            self.dismissal_tracker.record_confirm(alert_id)
        elif director_action == "dismiss":
            self.accuracy_tracker.record_miss(alert_id)
            self.dismissal_tracker.record_dismiss(alert_id)
        elif director_action == "dismiss_forever":
            self.dismissal_tracker.record_permanent_dismiss(alert_id)
```

---

## 10. DIRECTOR FACING COPY

Every alert includes:

```
⚠️  SCENE 5, SHOT 3, TAKE 4
WATCH CONTINUITY ISSUE

Watch switched from LEFT to RIGHT wrist at 01:34.
This is a CRITICAL prop — script requires left wrist
for continuity with Scene 23 payoff.

Confidence: 96%
Basis: YOLO detection (0.85) × Historical accuracy (0.95) × Director trust (1.00) = 0.96
Plot Weight: CRITICAL → Instant Alert

Evidence:
  • Scene 2 (Day 1): Watch on LEFT wrist — slate metadata
  • Scene 5 (Today): Watch on RIGHT wrist — YOLO frame 3637
  • Plot Graph: "watch must remain on left wrist (Scene 23 payoff)"

[Confirm] [Dismiss] [Dismiss & Don't Show Again]
```

---

## 11. EDGE CASES

| Scenario | Handling |
|----------|----------|
| **First-day shooting** | Historical accuracy defaults to 0.95. No penalty for being new. |
| **Director dismisses 3x in one hour** | Immediate deprioritization. Category muted for 48 hours. |
| **Critical prop + low confidence** | Escalate to Pro. If Pro also uncertain, SILENT LOG with "needs human review" flag. |
| **Multiple anomalies in one take** | Process independently. Bundle alerts if same prop, same scene. |
| **Anomaly contradicts previous alert** | Flag as "conflicting evidence" and escalate to Pro immediately. |
| **Network failure during Pro escalation** | Queue for retry. If still failing after 5 min, SILENT LOG with "analysis pending" tag. |
| **Director queries a suppressed finding** | Retrieve and display with "Low confidence — this may not be accurate" disclaimer. |
| **Budget blown + CRITICAL prop detected** | CRITICAL bypasses budget (safety override). All other categories blocked until budget resets. |

---

## 12. COST GUARDRAILS

| Guardrail | Value | Purpose |
|-----------|-------|---------|
| Max Pro escalations per day | 50 | Prevent runaway costs |
| Max Pro escalations per take | 2 | Don't spiral on one bad take |
| Min confidence for Pro | 0.40 | Don't waste Pro on garbage |
| Pro escalation budget % | 15% of takes | Hard ceiling |
| Flash-Lite timeout | 30 seconds | Fail fast, don't hang |
| Pro timeout | 60 seconds | Deep reasoning needs time, but not forever |

---

*Document version: 2.0*
*Status: LOCKED — Zero-Laptop Deliverable 4 (Patched)*
*Patches applied: Multiplicative Dampening Trap fixed (PlotWeight as gate), Dead-Code Budget Guard fixed (moved to top of function)*
*Last updated: August 2, 2026*
