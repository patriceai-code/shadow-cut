# SHADOW CUT — UI Wireframes & Design Specs
## Deliverable 8 | Zero-Laptop Execution | Agentic Cinema Hackathon

---

## 1. DESIGN PHILOSOPHY

### The Vibe
**"Cinematic Command Center."**

The UI should feel like something a director would actually want open on their iPad on set — dark, focused, high-contrast, with information hierarchy so clear that a glance tells you everything. No clutter. No admin-panel aesthetics. This is a creative tool, not a database.

### Core Principles
1. **Darkness first** — Film sets are dark. The UI must be comfortable in low-light environments.
2. **Alert-driven hierarchy** — The most important thing (the alert) dominates visual attention.
3. **Trust through transparency** — Every claim shows its evidence. Nothing is hidden behind clicks.
4. **Mobile-native** — Directors walk around set with phones/tablets. Desktop is secondary.
5. **Zero learning curve** — If it needs a tutorial, it's wrong.

---

## 2. DESIGN TOKENS

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| **bg-primary** | `#0a0a0f` | Main background (near-black with blue undertone) |
| **bg-secondary** | `#12121a` | Card backgrounds, panels |
| **bg-tertiary** | `#1a1a24` | Elevated surfaces, hover states |
| **bg-elevated** | `#222230` | Modals, dropdowns, chat bubbles (assistant) |
| **border-subtle** | `#2a2a3a` | Dividers, card borders |
| **border-focus** | `#3d3d55` | Focus rings, active states |
| **text-primary** | `#f0f0f5` | Headlines, primary content |
| **text-secondary** | `#a0a0b0` | Labels, timestamps, metadata |
| **text-muted** | `#6a6a7a` | Disabled, placeholder, incidental |
| **accent-cyan** | `#00d4ff` | Primary actions, links, active indicators |
| **accent-cyan-glow** | `rgba(0, 212, 255, 0.15)` | Glow effects, hover backgrounds |
| **severity-critical** | `#ff3366` | Critical alerts, errors |
| **severity-warning** | `#ffaa33` | Warnings, medium priority |
| **severity-info** | `#00d4ff` | Info, low priority, success states |
| **severity-success** | `#33ff99` | Confirmed, resolved, good status |
| **chart-line** | `#00d4ff` | Graphs, sparklines |
| **chart-fill** | `rgba(0, 212, 255, 0.1)` | Graph fills |

### Typography

| Token | Font | Size | Weight | Line-Height | Usage |
|-------|------|------|--------|-------------|-------|
| **font-display** | Inter | 32px | 700 | 1.1 | Page titles, hero numbers |
| **font-h1** | Inter | 24px | 600 | 1.2 | Section headers |
| **font-h2** | Inter | 18px | 600 | 1.3 | Card titles, alert headers |
| **font-h3** | Inter | 14px | 600 | 1.4 | Subsection labels |
| **font-body** | Inter | 14px | 400 | 1.5 | Body text, descriptions |
| **font-small** | Inter | 12px | 400 | 1.4 | Metadata, timestamps |
| **font-mono** | JetBrains Mono | 13px | 400 | 1.4 | Code, confidence scores, take IDs |
| **font-mono-small** | JetBrains Mono | 11px | 400 | 1.4 | Timestamps, technical metadata |

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| **space-xs** | 4px | Tight gaps, icon padding |
| **space-sm** | 8px | Inline spacing, small gaps |
| **space-md** | 16px | Card padding, section gaps |
| **space-lg** | 24px | Panel padding, major separations |
| **space-xl** | 32px | Page margins, section breaks |
| **space-2xl** | 48px | Hero spacing, major layout divisions |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| **radius-sm** | 6px | Buttons, small tags |
| **radius-md** | 10px | Cards, input fields |
| **radius-lg** | 16px | Modals, large panels |
| **radius-full** | 9999px | Pills, avatars, status dots |

### Shadows & Glows

| Token | Value | Usage |
|-------|-------|-------|
| **shadow-card** | `0 4px 24px rgba(0,0,0,0.4)` | Cards, panels |
| **shadow-elevated** | `0 8px 32px rgba(0,0,0,0.5)` | Modals, dropdowns |
| **glow-critical** | `0 0 20px rgba(255,51,102,0.3)` | Critical alert cards |
| **glow-warning** | `0 0 20px rgba(255,170,51,0.2)` | Warning alert cards |
| **glow-cyan** | `0 0 16px rgba(0,212,255,0.15)` | Active elements, focus |

---

## 3. LAYOUT ARCHITECTURE

### Screen Breakpoints

| Breakpoint | Width | Primary Device |
|------------|-------|----------------|
| **mobile** | 375px | Phone (director on set) |
| **tablet** | 768px | iPad (primary on-set device) |
| **desktop** | 1440px | DIT cart monitor, office review |

### Grid System

- **Mobile:** Single column, full-width cards, bottom nav bar
- **Tablet:** 2-column main grid (alerts left, chat right), collapsible sidebar
- **Desktop:** 3-column layout (nav sidebar | main feed | detail panel)

### Navigation Structure

```
┌─────────────────────────────────────────────────────────────┐
│  [LOGO]  Dashboard  Alerts  Chat  Trust Report  [Settings]  │  ← Top Nav (Desktop)
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MAIN CONTENT AREA                                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  [🏠]  [🔔]  [💬]  [📊]                                    │  ← Bottom Nav (Mobile)
└─────────────────────────────────────────────────────────────┘
```

**Mobile bottom nav (always visible):**
- 🏠 Dashboard (home)
- 🔔 Alerts (badge count)
- 💬 Chat (badge count)
- 📊 Trust Report

---

## 4. SCREEN 1: DASHBOARD (The Home Screen)

### Purpose
The director opens the app and immediately knows: What's happening right now? Are there issues? What's the status of today's shoot?

### Layout (Tablet — Primary Target)

```
┌─────────────────────────────────────────────────────────────────────┐
│  SHADOW CUT                              🎬 Scene 5 — The Confrontation│
│  The director still directs.              ⏱️ Day 3 of 18 | 2:34 PM   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  TODAY'S STATUS                    [Refresh ▶]              │   │
│  │                                                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │   47     │  │    3     │  │    0     │  │   100%   │   │   │
│  │  │  Takes   │  │  Alerts  │  │ Critical │  │ Accuracy │   │   │
│  │  │ Analyzed │  │  Today   │  │  Pending │  │  Score   │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────┐  ┌─────────────────────────────┐ │
│  │  🔔 RECENT ALERTS            │  │  📊 COVERAGE MAP            │ │
│  │                              │  │                             │ │
│  │  ┌────────────────────────┐  │  │      [Scene 1] ✅           │ │
│  │  │ ⚠️ WATCH MOVED         │  │  │      [Scene 2] ✅           │ │
│  │  │ Scene 5, Shot 3, T4    │  │  │      [Scene 3] ✅           │ │
│  │  │ Left → Right wrist     │  │  │      [Scene 4] 🎬           │ │
│  │  │ 96% confidence • 2m ago│  │  │      [Scene 5] ⚠️           │ │
│  │  └────────────────────────┘  │  │      [Scene 6] ⬜           │ │
│  │                              │  │      [Scene 7] ⬜           │ │
│  │  ┌────────────────────────┐  │  │                             │ │
│  │  │ ⚠️ LETTER OPENED       │  │  │  Legend: ✅ Done 🎬 Active  │ │
│  │  │ Scene 5, Shot 2, T2    │  │  │          ⚠️ Alert  ⬜ Todo  │ │
│  │  │ Folded → Open at 1:02  │  │  │                             │ │
│  │  │ 92% confidence • 5m ago│  │  └─────────────────────────────┘ │
│  │  └────────────────────────┘  │                                   │
│  │                              │  ┌─────────────────────────────┐ │
│  │  [View All Alerts →]         │  │  🎥 LIVE FEED               │ │
│  │                              │  │                             │ │
│  └──────────────────────────────┘  │  [Processing Take s5_sh3_t5]│ │
│                                    │  ████████████░░░░░░░░  62%  │ │
│                                    │                             │ │
│                                    │  YOLO → Flash-Lite → Alert? │ │
│                                    │                             │ │
│                                    └─────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Components

#### 4.1 Status Cards (Top Row)

```
┌─────────────────┐
│                 │
│      47         │  ← font-display, accent-cyan
│                 │
│   Takes         │  ← font-h3, text-secondary
│   Analyzed      │
│                 │
└─────────────────┘
- bg: bg-secondary
- border: 1px solid border-subtle
- radius: radius-md
- padding: space-lg
- width: ~22% each, flex row, gap: space-md
- Hover: border-color transitions to accent-cyan, subtle glow-cyan
```

**States:**
- Normal: border-subtle
- Active/Hover: border-focus + glow-cyan
- Alert present: Left border 3px solid severity-warning

#### 4.2 Coverage Map

```
- bg: bg-secondary
- border: 1px solid border-subtle
- radius: radius-md
- padding: space-lg

Scene blocks: 40px × 40px squares, gap: space-sm
- ✅ Done: bg-success at 20%, border-success, text-success
- 🎬 Active: bg-accent-cyan at 15%, border-accent-cyan, pulsing dot
- ⚠️ Alert: bg-critical at 20%, border-critical, text-critical
- ⬜ Todo: bg-tertiary, border-subtle, text-muted
```

**Pulsing active indicator:**
```css
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(0, 212, 255, 0); }
}
```

#### 4.3 Live Feed Card

```
- Shows current processing take
- Progress bar: bg-tertiary background, accent-cyan fill
- Pipeline stages: YOLO → Flash-Lite → Alert?
  - Completed stages: accent-cyan + checkmark
  - Current stage: pulsing accent-cyan
  - Pending stages: text-muted
- Cancel button (X) top-right for false starts
```

---

## 5. SCREEN 2: ALERT DETAIL (The Money Shot)

### Purpose
When the director taps an alert, they see the full evidence. This is the screen that proves Shadow Cut works. It must be visually stunning and instantly comprehensible.

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ⚠️  CONTINUITY ALERT                              [DISMISS]│   │
│  │       CRITICAL                                           [?]│   │
│  │                                                             │   │
│  │  Watch switched from LEFT to RIGHT wrist                    │   │
│  │  Scene 5, Shot 3, Take 4  •  01:34 into take                │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  CONFIDENCE: 96%                                    │   │   │
│  │  │  ████████████████████████████████████████████░░░░   │   │   │
│  │  │  Evidence: YOLO detection + Script rule match       │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  │  ┌─────────────────────────┐  ┌─────────────────────────┐  │   │
│  │  │  [FRAME]                │  │  [FRAME]                │  │   │
│  │  │  Take 2                 │  │  Take 4                 │  │   │
│  │  │  Watch: LEFT wrist      │  │  Watch: RIGHT wrist     │  │   │
│  │  │  ✅ Reference           │  │  │  ⚠️ Current            │  │   │
│  │  └─────────────────────────┘  └─────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  📋 SCRIPT RULE VIOLATED                            │   │   │
│  │  │                                                     │   │   │
│  │  │  "The watch must remain on Alex's left wrist        │   │   │
│  │  │   (established Scene 1, payoff Scene 23)."          │   │   │
│  │  │                                                     │   │   │
│  │  │  Source: Plot Knowledge Graph • Scene 5 context     │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  💬 DIRECTOR HISTORY                                │   │   │
│  │  │                                                     │   │   │
│  │  │  You've overridden 3/4 watch continuity alerts      │   │   │
│  │  │  for performance reasons. Still flagging because    │   │   │
│  │  │  this prop is CRITICAL.                             │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  │  [   Mark as Resolved   ]  [   Request Reshoot   ]         │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Alert Card Specs

#### Severity Levels

**CRITICAL:**
```
- Left border: 4px solid severity-critical
- Background: bg-secondary with subtle critical tint (rgba(255,51,102,0.05))
- Glow: glow-critical
- Icon: ⚠️ filled, severity-critical color
- Sound: Subtle notification chime (if enabled)
- Vibration: Short pulse (mobile)
```

**WARNING:**
```
- Left border: 4px solid severity-warning
- Background: bg-secondary with subtle warning tint (rgba(255,170,51,0.05))
- Glow: glow-warning
- Icon: ⚠️ outline, severity-warning color
- No sound/vibration
```

**INFO:**
```
- Left border: 4px solid severity-info
- Background: bg-secondary
- No glow
- Icon: ℹ️, severity-info color
```

#### Evidence Card (Script Rule)

```
- bg: bg-tertiary
- border-left: 3px solid accent-cyan
- radius: radius-md
- padding: space-md
- Contains:
  - Rule text in font-body, text-primary
  - Source metadata in font-small, text-muted
  - "Scene X context" link (tappable, navigates to scene)
```

#### Frame Comparison

```
- Two frames side-by-side (stacked on mobile)
- Each frame:
  - Rounded container (radius-md)
  - Label below: Take number, prop state
  - Status badge: ✅ Reference or ⚠️ Current
  - Bounding box overlay on prop (if available): 2px solid accent-cyan, 70% opacity
- Swipeable on mobile (carousel)
```

#### Action Buttons

```
Primary (Resolve):
- bg: severity-success
- text: bg-primary (dark)
- radius: radius-sm
- padding: 12px 24px
- font: font-h3
- Hover: brightness 1.1

Secondary (Reshoot):
- bg: transparent
- border: 1px solid severity-critical
- text: severity-critical
- radius: radius-sm
- padding: 12px 24px
- Hover: bg severity-critical at 10%

Tertiary (Dismiss):
- bg: transparent
- text: text-muted
- No border
- Hover: text-primary
```

---

## 6. SCREEN 3: CHAT INTERFACE (The Scripty)

### Purpose
The director's conversational interface to Shadow Memory. It should feel like texting a hyper-competent script supervisor who never sleeps.

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  💬 SHADOW CHAT                                          [Clear]    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  🟢 Shadow is online • 47 takes in memory                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────┐                        │
│  │ Which take did the letter stay folded  │  ← Director (right)   │
│  │ in Scene 14? I need one for the Scene  │                        │
│  │ 23 payoff.                             │                        │
│  │                                 2:41 PM │                        │
│  └────────────────────────────────────────┘                        │
│                                                                     │
│         ┌─────────────────────────────────────────────────────┐    │
│         │  📎 Scene 14, Shot 2:                               │    │
│         │                                                     │    │
│         │  • Take 1: Letter FOLDED (confidence: 0.91) ✅      │    │
│         │  • Take 2: Letter OPEN at 01:02 (confidence: 0.87) ❌│   │
│         │  • Take 3: Letter FOLDED (confidence: 0.89) ✅      │    │
│         │                                                     │    │
│         │  Recommendation: Use Take 1 or Take 3 for Scene 23  │    │
│         │  continuity. Take 2 shows the letter open — this    │    │
│         │  contradicts the payoff.                            │    │
│         │                                                     │    │
│         │  [View Take 1] [View Take 3]                        │    │
│         │                                          Shadow • 2:41 PM│
│         └─────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌────────────────────────────────────────┐                        │
│  │ What did I say about Scene 5 last      │  ← Director (right)   │
│  │ week?                                  │                        │
│  │                                 2:38 PM │                        │
│  └────────────────────────────────────────┘                        │
│                                                                     │
│         ┌─────────────────────────────────────────────────────┐    │
│         │  You circled Take 2 and said:                       │    │
│         │  "Love the energy, keep it."                        │    │
│         │                                                     │    │
│         │  You NG'd Take 4 for being "too theatrical."        │    │
│         │                                                     │    │
│         │  [🎵 Play audio note]                               │    │
│         │                                          Shadow • 2:38 PM│
│         └─────────────────────────────────────────────────────┘    │
│                                                                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  🔍 Ask anything about the shoot...              [Send ➤]  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Chat Bubble Specs

**Director Message (Right-aligned):**
```
- bg: accent-cyan
- text: bg-primary (dark)
- radius: radius-lg top-left, top-right, bottom-left (sharp bottom-right)
- padding: space-md
- max-width: 75%
- margin-left: auto (pushes right)
- Timestamp: font-mono-small, text-muted, right-aligned below
```

**Shadow Message (Left-aligned):**
```
- bg: bg-elevated
- text: text-primary
- border: 1px solid border-subtle
- radius: radius-lg top-right, top-left, bottom-right (sharp bottom-left)
- padding: space-md
- max-width: 85%
- margin-right: auto (pushes left)
- Timestamp: font-mono-small, text-muted, right-aligned below
- "Shadow" label: font-small, text-secondary, above bubble
```

**Quick Action Buttons (Inside Shadow bubbles):**
```
- bg: bg-tertiary
- border: 1px solid border-subtle
- text: accent-cyan
- radius: radius-sm
- padding: 6px 12px
- font: font-small
- Hover: border-accent-cyan, bg accent-cyan-glow
```

#### Input Bar

```
- bg: bg-secondary
- border-top: 1px solid border-subtle
- padding: space-md
- Input field:
  - bg: bg-tertiary
  - border: 1px solid border-subtle
  - radius: radius-full
  - padding: 12px 16px
  - placeholder: "Ask anything about the shoot..."
  - Focus: border-accent-cyan, glow-cyan
- Send button:
  - bg: accent-cyan
  - text: bg-primary
  - radius: radius-full
  - 40px × 40px circle
  - Icon: paper airplane
  - Disabled state: bg-tertiary, text-muted
```

#### Suggested Prompts (Empty State)

When chat is empty, show quick-start chips:
```
"What did I say about Scene 5?"
"Did the watch move?"
"Are we missing coverage?"
"Show me flagged takes from today"
```

---

## 7. SCREEN 4: TRUST REPORT (The Closer)

### Purpose
The screen that makes producers and judges go "holy shit." It shows Shadow's accuracy, cost, and ROI in beautiful, undeniable numbers.

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  ← Back                              📊 SHADOW TRUST REPORT         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PRODUCTION: "The Last Take"                                │   │
│  │  Day 5 of 18  •  47 takes analyzed                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐│
│  │  ACCURACY SCORE              │  │  COST TRACKER                ││
│  │                              │  │                              ││
│  │        ┌──────────┐          │  │   API Cost So Far            ││
│  │       /    96%    \         │  │   ━━━━━━━━━━━━━━━━━━         ││
│  │      /   ██████    \        │  │        $0.56                 ││
│  │     │   ████████   │         │  │                              ││
│  │      \   ██████   /         │  │   Est. Total (500 takes)     ││
│  │       \──────────/          │  │   ━━━━━━━━━━━━━━━━━━         ││
│  │                              │  │        $7.00                 ││
│  │  47 takes • 3 alerts         │  │                              ││
│  │  3 confirmed • 0 false       │  │   vs. Script Supervisor      ││
│  │                              │  │        $12,000               ││
│  └──────────────────────────────┘  └──────────────────────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ALERT BREAKDOWN                                            │   │
│  │                                                             │   │
│  │  Prop Continuity    ████████████████████░░░░░░░░░░  12      │   │
│  │  Performance        ██████░░░░░░░░░░░░░░░░░░░░░░░░   3      │   │
│  │  Missing Coverage   ███░░░░░░░░░░░░░░░░░░░░░░░░░░░   2      │   │
│  │  Audio Issues       █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   1      │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  💰 ROI CALCULATOR                                          │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │                                                     │   │   │
│  │  │   If Shadow prevents 1 reshoot day:    $50,000      │   │   │
│  │  │   Shadow Cut cost for entire film:         $7       │   │   │
│  │  │                                                     │   │   │
│  │  │   RETURN ON INVESTMENT:              7,142x         │   │   │
│  │  │                                                     │   │   │
│  │  │   [Learn more →]                                    │   │   │
│  │  │                                                     │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  📈 ACCURACY OVER TIME                                      │   │
│  │                                                             │   │
│  │    100% │                                        ●──●       │   │
│  │     90% │                              ●──●──●               │   │
│  │     80% │                    ●──●──●                         │   │
│  │     70% │          ●──●                                      │   │
│  │     60% │    ●──●                                              │   │
│  │        └──────────────────────────────────────────────────    │   │
│  │         Day 1   Day 2   Day 3   Day 4   Day 5                │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Specs

#### Accuracy Donut Chart

```
- SVG-based donut chart
- Stroke width: 12px
- Background ring: bg-tertiary
- Fill ring: gradient from accent-cyan to #0088aa
- Center text: font-display, text-primary
- Subtext: font-body, text-secondary
- Animation: Fill animates from 0% to actual% on load (1s ease-out)
```

#### Cost Tracker

```
- Large number: font-display, accent-cyan
- Comparison number: font-h2, text-muted (strikethrough for script supervisor cost)
- Savings badge: "Saves $11,993" in severity-success pill
```

#### ROI Hero Card

```
- bg: gradient from bg-secondary to bg-tertiary (subtle)
- border: 1px solid border-subtle
- radius: radius-lg
- padding: space-xl
- Centered content
- The "7,142x" number: font-display, severity-success, slight glow
- "RETURN ON INVESTMENT" label: font-h3, text-secondary, letter-spacing 2px
```

#### Bar Charts

```
- Horizontal bars
- Bar height: 24px
- Bar radius: radius-sm
- Colors by category:
  - Prop Continuity: accent-cyan
  - Performance: severity-warning
  - Missing Coverage: severity-info
  - Audio: text-muted
- Background track: bg-tertiary
- Count label: font-mono, text-primary, right-aligned
```

#### Line Graph (Accuracy Over Time)

```
- SVG line chart
- Line: 3px stroke, accent-cyan
- Fill: gradient accent-cyan to transparent (10% opacity)
- Dots: 8px circles, bg-accent-cyan, border 2px bg-secondary
- Grid lines: 1px border-subtle, horizontal only
- Labels: font-mono-small, text-secondary
- Animation: Line draws from left to right on scroll into view
```

---

## 8. SCREEN 5: SETTINGS & ONBOARDING

### Onboarding Flow (First Launch)

```
Step 1: Upload Script
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              📄                                             │
│                                                             │
│         Upload Your Script                                  │
│                                                             │
│    Shadow will read the entire script and build a           │
│    Plot Knowledge Graph — identifying critical props,       │
│    emotional arcs, and setup/payoff links.                  │
│                                                             │
│    ┌─────────────────────────────────────────────────┐     │
│    │  Drag script here (PDF, Fountain, TXT)          │     │
│    │                                                 │     │
│    │         [or browse files]                       │     │
│    └─────────────────────────────────────────────────┘     │
│                                                             │
│                   [Continue →]                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Step 2: Processing
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│         ⚡ Processing Script...                             │
│                                                             │
│         ████████████████████████████████░░░░  84%          │
│                                                             │
│         Extracting scenes...                                │
│         Identifying props...                                │
│         Mapping emotional arcs...                           │
│         Building continuity rules...                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Step 3: Ready
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│         ✅ Script Loaded                                    │
│                                                             │
│         12 scenes • 8 critical props • 3 emotional arcs     │
│                                                             │
│         Shadow is ready for Day 1.                          │
│                                                             │
│              [Go to Dashboard →]                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Settings Screen

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ SETTINGS                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  NOTIFICATIONS                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Critical Alerts                    [Toggle: ON 🟢] │   │
│  │  Warning Alerts                     [Toggle: ON 🟢] │   │
│  │  Info Alerts                        [Toggle: OFF ⚪]│   │
│  │  Sound Effects                      [Toggle: ON 🟢] │   │
│  │  Vibration (Mobile)                 [Toggle: ON 🟢] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ALERT THRESHOLDS                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Minimum Confidence for Alert                       │   │
│  │  [━━━━●━━━━━━━━━━━━━]  75%                          │   │
│  │                                                     │   │
│  │  Auto-escalate Critical Props                       │   │
│  │  [Toggle: ON 🟢]                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ACCOUNT                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Production: "The Last Take"                        │   │
│  │  Role: Director                                     │   │
│  │  [Disconnect Production]                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Toggle Switch

```
- Track: 44px × 24px, radius-full
- OFF: bg-tertiary, knob at left (20px circle, bg-muted)
- ON: bg-accent-cyan, knob at right (20px circle, bg-primary)
- Transition: 200ms ease
- Tap target: 44px × 44px (accessible)
```

#### Slider

```
- Track: 4px height, bg-tertiary, radius-full
- Fill: accent-cyan
- Thumb: 20px circle, bg-primary, border 2px accent-cyan
- Active: glow-cyan
- Value label: font-mono, text-primary, right of slider
```

---

## 9. COMPONENT LIBRARY

### Buttons

| Variant | Background | Text | Border | Hover |
|---------|-----------|------|--------|-------|
| **Primary** | accent-cyan | bg-primary | none | brightness 1.1, glow-cyan |
| **Secondary** | transparent | accent-cyan | 1px accent-cyan | bg accent-cyan-glow |
| **Danger** | transparent | severity-critical | 1px severity-critical | bg severity-critical at 10% |
| **Ghost** | transparent | text-secondary | none | text-primary |
| **Icon** | bg-tertiary | text-secondary | none | bg bg-elevated, text-primary |

### Cards

```
Base Card:
- bg: bg-secondary
- border: 1px solid border-subtle
- radius: radius-md
- padding: space-lg
- shadow: shadow-card

Alert Card (extends Base):
- Left border: 3-4px severity color
- Optional glow based on severity

Stat Card (extends Base):
- Centered content
- Number: font-display
- Label: font-h3, text-secondary
- Hover: border-accent-cyan
```

### Badges / Pills

```
- padding: 4px 10px
- radius: radius-full
- font: font-small

Status badges:
- Processing: bg accent-cyan at 15%, text accent-cyan
- Complete: bg severity-success at 15%, text severity-success
- Error: bg severity-critical at 15%, text severity-critical
- Warning: bg severity-warning at 15%, text severity-warning
```

### Progress Indicators

```
Linear:
- Height: 4px (subtle) or 8px (prominent)
- Track: bg-tertiary
- Fill: accent-cyan
- radius: radius-full

Circular (processing):
- 40px diameter
- Stroke: 3px accent-cyan
- Animation: rotate 360° 1s linear infinite

Pipeline Steps:
- Horizontal row of dots/labels
- Completed: accent-cyan + checkmark
- Current: pulsing accent-cyan dot
- Pending: text-muted
- Connector line: 2px, completed=accent-cyan, pending=bg-tertiary
```

---

## 10. ANIMATIONS & MICRO-INTERACTIONS

### Principles
- **Purposeful:** Every animation communicates state change
- **Fast:** 200-300ms max. Directors don't wait.
- **Subtle:** Never flashy. Professional tools whisper, don't shout.

### Alert Entrance

```
Duration: 400ms
Easing: cubic-bezier(0.16, 1, 0.3, 1)

From:
  opacity: 0
  transform: translateY(-20px) scale(0.95)
To:
  opacity: 1
  transform: translateY(0) scale(1)

Plus: glow fades in over 600ms
```

### Card Hover (Desktop)

```
Duration: 200ms
Easing: ease-out

Border color: border-subtle → border-focus
transform: translateY(-2px)
shadow: shadow-card → shadow-elevated
```

### Chat Message Entrance

```
Director message:
  From: opacity 0, translateX(20px)
  To: opacity 1, translateX(0)
  Duration: 300ms

Shadow message:
  From: opacity 0, translateX(-20px)
  To: opacity 1, translateX(0)
  Duration: 300ms
  Delay: 100ms (thinking pause)
```

### Skeleton Loading

```
- bg: linear-gradient(90deg, bg-tertiary 25%, bg-elevated 50%, bg-tertiary 75%)
- background-size: 200% 100%
- animation: shimmer 1.5s infinite

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Number Count-Up

```
- Duration: 1.5s
- Easing: ease-out
- Trigger: On scroll into view
- Format: Integers count up. Currency adds "$". Percentages add "%".
```

---

## 11. MOBILE-SPECIFIC CONSIDERATIONS

### Bottom Sheet (Alert Detail on Mobile)

Instead of a full page, alerts open as a bottom sheet:

```
- Height: 85% of screen
- bg: bg-secondary
- radius: radius-lg top corners only
- Handle bar: 40px × 4px, bg-muted, centered at top
- Swipe down to dismiss
- Scrollable content
- Backdrop: bg-primary at 70% opacity
```

### Thumb Zones

```
All primary actions within bottom 25% of screen:
- Dismiss button: bottom-left
- Resolve button: bottom-right (primary action, easiest reach)
- Chat send: bottom-right
```

### Haptic Feedback

```
- Critical alert: Heavy impact + notification sound
- Warning: Light impact
- Message received: Light impact
- Button tap: Selection feedback
```

### Pull-to-Refresh

```
- Dashboard: Pull down to refresh status
- Chat: Pull down to load older messages
- Visual: Circular spinner, accent-cyan
```

---

## 12. DEMO VIDEO UI REQUIREMENTS

For the 3-minute demo video, the UI must look **polished, not prototyped.**

### Critical Visual Rules

1. **No placeholder text** — Use real production names ("The Last Take"), real names ("Alex", "Morgan"), real timestamps.
2. **No Lorem Ipsum** — Every alert must have a real script rule. Every chat message must make sense.
3. **Consistent data** — If Take 2 has the watch on the left wrist in the alert, the chat must reference the same take.
4. **Smooth animations** — Alerts should slide in. Numbers should count up. Progress bars should fill.
5. **No empty states** — The demo shows a production on Day 5. The dashboard is populated. The chat has history.
6. **High contrast** — Viewed on YouTube compression, the UI must still read clearly. Test at 480p.

### 🎬 DEMO VIDEO RECORDING RULE (CRITICAL)

**Record ONLY in landscape orientation. Never portrait.**

| Layout | Resolution | Use In Demo? | Why |
|--------|-----------|--------------|-----|
| **Desktop (3-column)** | 1440×900 | ✅ PRIMARY | Fills 16:9 YouTube frame. All cards, graphs, and frame comparisons are legible at 480p. |
| **Tablet (landscape)** | 1024×768 | ✅ ACCEPTABLE | Good fallback if desktop layout feels too wide. Still fills 16:9 with minimal black bars. |
| **Mobile (portrait)** | 375×812 | ❌ NEVER | Massive black bars on YouTube. font-small and font-mono-small become unreadable. Judges will squint and skip. |

**Recording Setup:**
- Browser viewport: 1440×900 (desktop) or 1024×768 (tablet)
- OBS canvas: 1920×1080 (16:9)
- UI centered in frame with subtle dark background fill
- No device frames, no phone mockups — just the UI filling the screen

**Why this matters:**
Hackathon judges watch on laptops. A vertical phone recording at 9:16 gets pillarboxed into a tiny center column. Your beautiful alert cards, confidence percentages, and frame comparisons shrink to unreadable sizes. The ROI dashboard — your killer closing — becomes a blurry smear.

**The mobile layouts in this spec are for the real product.** Directors on set use them. But the demo video is a sales pitch, not a user test. Every pixel of the 16:9 frame must sell the product.

### Demo-Specific Mock Data

```
Production Name: "The Last Take"
Director: "You" (first-person perspective)
Current Scene: Scene 5 — "The Confrontation"
Day: 5 of 18
Time: 2:34 PM

Key demo props:
- watch (CRITICAL, left wrist, Scene 1→23)
- letter (CRITICAL, folded, Scene 5→23)
- coffee cup (INCIDENTAL)

Demo takes to show:
- s5_sh3_t2: Watch LEFT wrist (reference)
- s5_sh3_t4: Watch RIGHT wrist (ALERT)
- s5_sh2_t2: Letter OPEN (ALERT)
```

---

## 13. ACCESSIBILITY

### Minimum Standards

- **Color contrast:** All text meets WCAG AA (4.5:1 for body, 3:1 for large text)
- **Touch targets:** Minimum 44px × 44px
- **Focus indicators:** Visible focus rings (glow-cyan) for keyboard navigation
- **Screen reader:** All icons have aria-labels. Alert cards read severity first.
- **Reduced motion:** Respect `prefers-reduced-motion` — disable shimmer, pulse, and slide animations

### Alert Accessibility

```
aria-live="polite" on alert container
aria-label="Critical continuity alert: Watch moved from left to right wrist"
Role: "alert" for critical, "status" for warning/info
```

---

## 14. FILE DELIVERABLES

| File | Format | Purpose |
|------|--------|---------|
| `ui_wireframes.md` | Markdown | This document — full spec |
| `design_tokens.css` | CSS | Color, type, spacing variables |
| `component_library.fig` | Figma | Visual components (if Figma available) |
| `demo_mock_data.json` | JSON | All data shown in demo video |

---

*Document Status: LOCKED*
*Deliverable: 8 of 10*
*Next: README & Setup Documentation (Deliverable 9)*
