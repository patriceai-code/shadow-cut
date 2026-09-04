# Shadow Cut — Plot Knowledge Graph Edge Cases
## How to Handle Ambiguous Script Elements

---

## 1. IMPLIED PROPS

**Definition:** Objects that are referenced through action rather than explicit description.

**Examples:**
- "She glanced at her father's watch" → `watch` is a prop
- "He poured himself a drink" → `glass` + `liquor` are props
- "She checked her phone" → `phone` is a prop
- "They sat at the table" → `table` is INCIDENTAL, `chairs` are INCIDENTAL

**Rule:** If a character interacts with an object (touches, looks at, uses, holds), it is a prop. If the object is merely part of the setting (wall, floor, sky), it is not.

**Classification:**
- If the interaction reveals character or plot → IMPORTANT or CRITICAL
- If the interaction is routine (sitting in chair, walking on floor) → INCIDENTAL or ignore

---

## 2. OFF-SCREEN MENTIONS

**Definition:** Props or setups mentioned in dialogue but not physically present in the scene.

**Examples:**
- "The letter is in my desk" (Scene 5) → `letter` is CRITICAL, referenced but not visible
- "I left the gun in the car" → `gun` is CRITICAL, establishes location for later
- "Remember the watch Dad gave me?" → `watch` is CRITICAL, emotional significance

**Rule:** Off-screen mentions of CRITICAL props must be tracked. The prop may appear in a later scene, and its state must match the off-screen reference.

**Schema handling:**
```json
{
  "prop_name": "letter",
  "scene_state": "referenced_only",
  "rules": ["Must be in desk drawer per dialogue in Scene 5"],
  "physically_present": false
}
```

---

## 3. TRANSFORMING PROPS

**Definition:** Props that change their fundamental nature during the film.

**Examples:**
- A letter that starts folded, gets opened, then burned
- A photograph that gets torn in half
- A weapon that gets fired, then discarded
- A cake that gets cut, then eaten

**Rule:** Track the transformation chain. Each state change is a potential continuity trap.

**State vocabulary must include ALL states:**
```json
"state_vocabulary": ["folded", "partially_open", "fully_open", "burned", "ashes"]
```

**Alert logic:**
- If state jumps backward (burned → folded) → CRITICAL ALERT
- If state skips forward without intermediate (folded → ashes) → WARNING (missing coverage)

---

## 4. SHARED / TRANSFERRED PROPS

**Definition:** Props that move between characters or locations.

**Examples:**
- "They both reach for the gun" → Who ends up with it?
- "She handed him the letter" → Transfer from Character A to B
- "The briefcase sits on the table" → Available to all characters

**Rule:** Track possession per scene. A prop transfer is a CRITICAL continuity event.

**Schema handling:**
```json
{
  "prop_name": "letter",
  "scene_state": "held_by_Character_B",
  "rules": ["Transferred from Character_A in this scene"],
  "possession": {
    "holder": "Character_B",
    "previous_holder": "Character_A",
    "transfer_frame": 2450
  }
}
```

---

## 5. TEMPORAL / TIME-SENSITIVE PROPS

**Definition:** Props whose state depends on time of day or scene order.

**Examples:**
- "Morning coffee" in Scene 3, "Cold coffee" in Scene 8
- "Lit cigarette" that should burn down over time
- "Melting ice" in a drink
- "Setting sun" visible through window (lighting continuity)

**Rule:** Time-sensitive props require state tracking across non-sequential shooting. The Shadow must know: "This scene is set at 8am, so the coffee should be full and steaming, not half-empty."

**Schema handling:**
```json
{
  "prop_name": "coffee_cup",
  "scene_state": "full_steam",
  "rules": ["Scene is set at 8am — coffee should be freshly poured"],
  "time_context": "morning"
}
```

---

## 6. COSTUME AS PROP

**Definition:** Clothing or accessories that have plot significance beyond mere costume.

**Examples:**
- "Her red scarf — the one from the accident" → CRITICAL prop (plot significance)
- "His lucky jacket" → IMPORTANT prop (character signature)
- "A business suit" → INCIDENTAL (generic costume)
- "The torn dress from the fight" → CRITICAL (must remain torn in subsequent scenes)

**Rule:** If the script calls attention to a clothing item, it's a prop. If it's just "Alex wears a shirt," it's costume.

**Decision matrix:**
| Criterion | Costume | Prop |
|-----------|---------|------|
| Script names it specifically | No | Yes |
| Has emotional significance | No | Yes |
| Changes state (torn, bloody, lost) | No | Yes |
| Setup/payoff relevance | No | Yes |
| Character signature | Maybe | Yes |

---

## 7. ANIMALS & LIVING PROPS

**Definition:** Animals or living things with continuity requirements.

**Examples:**
- "The dog must be on the leash in Scene 3" → `dog` + `leash` are CRITICAL
- "The bird in the cage" → `bird` is IMPORTANT (must stay in cage until released)
- "A fly on the wall" → INCIDENTAL (ignore)

**Rule:** Animals with scripted behavior or state requirements are props. Background wildlife is not.

---

## 8. WEATHER & ENVIRONMENT

**Definition:** Atmospheric conditions that affect continuity.

**Examples:**
- "Rain starts in Scene 8" → Continuity rule for Scene 8 and all subsequent scenes until "rain stops"
- "Snow on the ground" → Must persist in all outdoor scenes until melted
- "Foggy morning" → Must match in all scenes set at that time

**Rule:** Weather is NOT a prop. It is a scene-level continuity rule that affects all outdoor scenes in a time block.

**Schema handling:**
```json
{
  "scene": 8,
  "continuity_rules": [
    "Rain begins in this scene",
    "All subsequent outdoor scenes must show rain until Scene 15 (rain stops)"
  ]
}
```

---

## 9. LIGHTING CONTINUITY

**Definition:** Lighting conditions that must match across takes and scenes.

**Examples:**
- "Golden hour" → All shots in this scene must match golden hour lighting
- "Harsh overhead, shadows" → Must be consistent across all takes of this scene
- "Cold blue, underlit" → Must match in close-ups and wide shots

**Rule:** Lighting notes are scene-level continuity rules. They don't trigger prop alerts but may trigger scene-level warnings if Gemini detects lighting mismatches.

---

## 10. EMOTIONAL CONTINUITY (The Invisible Prop)

**Definition:** Actor emotional states that must match across non-sequential shooting.

**Examples:**
- Scene 20 (breakup) shot on Day 1 → Actor must be devastated
- Scene 15 (argument leading to breakup) shot on Day 18 → Actor must build TO devastation, not start there
- Scene 22 (recovery) shot on Day 5 → Actor must show early signs of recovery

**Rule:** Emotional arcs are tracked per character. The Shadow warns if a performance contradicts the established arc.

**This is NOT a prop alert.** It is a performance note flagged at MEDIUM confidence because it requires subjective judgment.

---

## 11. DUPLICATE / MULTIPLE INSTANCES

**Definition:** Multiple identical props that might be confused.

**Examples:**
- "Two coffee cups on the table" → Must track which character drinks from which
- "A row of identical guns" → Must track which one was fired
- "Multiple letters" → Must distinguish Letter A from Letter B

**Rule:** If multiples exist, assign identifiers (letter_A, letter_B) or track by association (cup_Alex, cup_Morgan).

---

## 12. DESTROYED / CONSUMED PROPS

**Definition:** Props that cease to exist during the film.

**Examples:**
- "The letter burns" → letter transitions to ashes, then no longer exists
- "He eats the apple" → apple is consumed, should not appear again
- "The vase shatters" → vase becomes shards, then is cleaned up

**Rule:** A destroyed prop should trigger a WARNING if it reappears intact in a later scene.

---

## DECISION MATRIX: CRITICAL vs IMPORTANT vs INCIDENTAL

| Question | CRITICAL | IMPORTANT | INCIDENTAL |
|----------|----------|-----------|------------|
| If this changed, would the audience notice? | Yes, immediately | Maybe, on rewatch | No |
| If this changed, would the plot break? | Yes | Maybe | No |
| Is this a setup for a later payoff? | Yes | Sometimes | No |
| Is this a character signature? | Yes | Sometimes | No |
| Does the script call special attention to it? | Yes | Maybe | No |
| Is it mentioned in more than 2 scenes? | Usually | Sometimes | Rarely |
| Would a reshoot be required to fix? | Yes | Maybe | No |

**Default rule:** When in doubt, classify UP (more important). A false alert on an IMPORTANT prop is better than missing a CRITICAL one.

---

## CONFIDENCE SCORING FOR EDGE CASES

| Edge Case Type | YOLO Confidence | Flash-Lite Confidence | Pro Escalation? |
|----------------|-----------------|----------------------|-----------------|
| Implied prop | N/A (no visual) | 0.60 (inferred) | No |
| Off-screen mention | N/A | 0.95 (script-verified) | No |
| Transforming prop | 0.85 (state detect) | 0.75 (semantic) | If CRITICAL |
| Shared prop | 0.80 (possession) | 0.70 (context) | If CRITICAL |
| Temporal prop | 0.70 (visual) | 0.65 (inferred) | No |
| Costume-as-prop | 0.75 (visual) | 0.80 (script context) | If signature |
| Animal prop | 0.70 (visual) | 0.65 (behavior) | No |
| Weather | N/A | 0.60 (scene context) | No |
| Emotional continuity | N/A | 0.55 (subjective) | Never alert, only log |
| Duplicate instances | 0.75 (tracking) | 0.70 (context) | No |
| Destroyed prop | 0.80 (absence) | 0.85 (script rule) | If reappears |

---

*Document version: August 2, 2026*
*Status: Locked for Bob Week implementation*
