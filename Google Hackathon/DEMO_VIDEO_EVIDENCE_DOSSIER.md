# SHADOW CUT — Demo Video Script & Forensic Evidence Dossier
## Official Hackathon Submission Artifact | Agentic Cinema (Devpost)

---

## 🎬 PART 1: 3-MINUTE TRAILER & DEMO VIDEO SCRIPT

### [0:00 - 0:30] THE HOOK: The Million-Dollar Reshoot Problem
- **Visual**: Dramatic footage of film slate cutting. Cut to George A. Romero's *Night of the Living Dead* (1968).
- **Voiceover (Director / Zach)**: 
  > *"On a film set, missing a single continuity error can cost an indie or studio production upwards of $100,000 in pickup reshoots. Today, human script supervisors still track thousands of props, wardrobe states, and lighting setups by hand in chaotic environments.*
  > *Meet **Shadow Cut** — the autonomous, real-time script supervisor that watches every take as it's filmed, cross-references the original shooting screenplay, and flags objective continuity breaks while leaving the director in total creative control."*

---

### [0:30 - 1:15] THE ARCHITECTURE: Screenplay-Grounded Intelligence
- **Visual**: Architecture schematic showing Screenplay $\rightarrow$ YOLO-World $\rightarrow$ Gemini 3.5 Flash-Lite $\rightarrow$ IBM Watsonx.
- **Voiceover**:
  > *"Shadow Cut doesn't guess from isolated video clips. It ingests the **actual shooting screenplay** into a structured Plot Knowledge Graph before cameras roll:*
  > 1. **Tier 1 (Edge Tracking)**: Local YOLO-World spatial tracking on CPU at 1 fps with zero latency.
  > 2. **Tier 2 (Multimodal Reasoning)**: 20-minute native video streams to **Gemini 3.5 Flash-Lite** to compare the filmed reality against the written text across all 142 cuts.
  > 3. **Director Autonomy Engine**: The AI never dictates creative choices. It classifies issues into **RETAKE REQUIRED**, **DIRECTOR REVIEW REQUIRED**, or **LOG ONLY**, giving the filmmaker instant interactive controls.
  > 4. **IBM Track Integration**: Built and orchestrated with IBM Bob and Watsonx MCP tools to manage take memory and automated production trust reports."*

---

### [1:15 - 2:15] THE HERO AUDIT: 20 Minutes of Real Cinema History
- **Visual**: Video player scrubbing through `test_data/notld/farmhouse_scene_full.mp4` with side-by-side forensic evidence cards.
- **Voiceover**:
  > *"We tested Shadow Cut against the complete, continuous 20-minute Farmhouse Siege sequence from Romero's 1968 classic, evaluating **142 cuts** against the authentic shooting script.*
  > *First, it flagged a **RETAKE REQUIRED** at **09:41** with **99% confidence** — detecting visible carpenter handwriting and measurements written directly on the barricade planks before being nailed to the window frame.*
  > *Second, it performed true script supervision: noticing at **00:00** that Duane Jones disregarded the scripted iron tire iron to wrench the oak dining table apart with his bare hands — an intentional actor performance choice the director can **Accept Risk** on.*
  > *Third, it caught genuine physical discrepancies: the 'Charcoal Lighter' fluid container shifting position between the fireplace hearth and chair, and subtle key-light contrast shifts on Harry Cooper as he emerges from the cellar."*

---

### [2:15 - 3:00] THE COMMAND CENTER: Real-Time Director Experience
- **Visual**: Live interactive walkthrough of the Next.js Cinematic Dashboard running on `localhost:3000`.
- **Voiceover**:
  > *"On set, the director interacts through our dark-mode Cinematic Command Center:*
  > - **The Dashboard**: Live status cards showing 142 cuts analyzed, 1 Critical Retake alert, 1 Review item, and 82% continuity health.
  > - **Continuity Queue**: Side-by-side visual forensic frames with instant **[Retake Take]**, **[Accept Risk]**, and **[Dismiss]** buttons.
  > - **Script Deviations Tab**: Clear comparison between what was written on the page vs what was performed on camera.
  > - **Chat with Shadow**: A natural language direct line to the AI, backed by Firestore and Gemini 3.5 memory.
  > - **The Trust Report**: Demonstrating **$45,000 in reshoot savings** achieved for an API compute cost of just **$0.046**.
  > *Shadow Cut: The director still directs. Shadow catches the rest."*

---

## 🔍 PART 2: FORENSIC CONTINUITY EVIDENCE DOSSIER

### 1. 🚨 Critical Alert: RETAKE REQUIRED
- **Film Timestamp**: `09:41` | **Clip Timestamp**: `09:41`
- **Category**: Set Construction Prop Flaw
- **Action Required**: **`RETAKE REQUIRED`**
- **Confidence Score**: **`99%`** (`0.99`)
- **Visual Proof**: During the close-up shot of Ben nailing horizontal reinforcement planks across the window/door frame, visible handwritten numbers and carpenter markings are present on the raw lumber facing the camera.
- **Technical Impact**: Breaches the cinematic fourth wall by revealing set construction materials directly on camera.
- **Evidence Frame**: [`test_data/notld/evidence_frames/01_retake_plank_markings_0941.jpg`](file:///c:/Users/zache/ShadowCut/test_data/notld/evidence_frames/01_retake_plank_markings_0941.jpg)

---

### 2. ⚠️ Warning Alert: DIRECTOR REVIEW REQUIRED

#### Charcoal Lighter Fluid Container Placement
- **Film Timestamp**: `07:58` | **Clip Timestamp**: `07:58`
- **Category**: Prop Continuity
- **Action Required**: **`DIRECTOR REVIEW REQUIRED`**
- **Confidence Score**: **`95%`** (`0.95`)
- **Visual Proof**: The rectangular 'Charcoal Lighter' fluid container position shifts slightly across cuts near the fireplace and chair.
- **Technical Impact**: Spatial discontinuity in prop handling during torch preparation.
- **Evidence Frame**: [`test_data/notld/evidence_frames/02_review_charcoal_lighter_0758.jpg`](file:///c:/Users/zache/ShadowCut/test_data/notld/evidence_frames/02_review_charcoal_lighter_0758.jpg)

---

### 3. 📋 Minor Alert: LOG ONLY (Natural Lighting Shift)

#### Key-Light Contrast Shift on Harry Cooper
- **Film Timestamp**: `15:33` | **Clip Timestamp**: `15:33`
- **Category**: Lighting Continuity
- **Action Required**: **`LOG ONLY`**
- **Confidence Score**: **`91%`** (`0.91`)
- **Visual Proof**: Noticeable contrast and shadow intensity shift on Harry Cooper's face between the initial cellar door emergence and subsequent argument cuts.
- **Technical Impact**: Multi-camera lighting variation common in low-budget black-and-white cinematography.
- **Evidence Frame**: [`test_data/notld/evidence_frames/03_log_cooper_lighting_1533.jpg`](file:///c:/Users/zache/ShadowCut/test_data/notld/evidence_frames/03_log_cooper_lighting_1533.jpg)

---

### 4. 📜 Screenplay Deviations (Written vs Performed)

#### Table Dismantling Action
- **Film Timestamp**: `00:00` | **Clip Timestamp**: `00:00`
- **Scripted**: *"Ben begins wrenching off table legs and planks using an iron tire iron and hammer."*
- **Filmed Reality**: Ben forcefully rips and kicks the table apart using his bare hands and body weight without any visible tire iron or hammer.
- **Director Action**: **`ACCEPT RISK`** (Physical struggle reads intensely on camera; minor tool inventory divergence).
- **Evidence Frame**: [`test_data/notld/evidence_frames/04_script_deviation_table_0045.jpg`](file:///c:/Users/zache/ShadowCut/test_data/notld/evidence_frames/04_script_deviation_table_0045.jpg)
