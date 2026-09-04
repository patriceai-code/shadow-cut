"""
Build high-definition 1920x1080 cinematic title and evidence cards for the demo video using Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("demo_production/graphics")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_header_badges(draw, category_text, badge_color=(59, 130, 246)):
    # Top brand bar
    draw.rectangle([(60, 40), (220, 75)], fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    draw.text((75, 48), "SHADOW CUT", font=get_font(FONT_BOLD, 18), fill=(241, 245, 249))
    draw.rectangle([(230, 40), (370, 75)], fill=badge_color)
    draw.text((245, 48), category_text, font=get_font(FONT_BOLD, 16), fill=(255, 255, 255))

def create_intro_title():
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)

    # Subtle ambient gradients / borders
    draw.rectangle([(60, 60), (1860, 1020)], outline=(30, 41, 59), width=2)
    draw.rectangle([(70, 70), (1850, 1010)], outline=(15, 23, 42), width=1)

    # Pill badge
    draw.rounded_rectangle([(780, 180), (1140, 225)], radius=20, fill=(30, 41, 59), outline=(59, 130, 246), width=2)
    draw.text((810, 192), "AGENTIC CINEMA 2026", font=get_font(FONT_BOLD, 18), fill=(96, 165, 250))

    # Main Title
    draw.text((960, 360), "SHADOW CUT", font=get_font(FONT_BOLD, 96), fill=(255, 255, 255), anchor="mm")
    
    # Subtitle
    draw.text((960, 470), "Autonomous On-Set AI Script Supervisor for Film Production", font=get_font(FONT_REGULAR, 32), fill=(148, 163, 184), anchor="mm")

    # Tagline in glowing gold
    draw.text((960, 580), '"The director still directs. The Shadow just remembers."', font=get_font(FONT_BOLD, 36), fill=(245, 158, 11), anchor="mm")

    # Bottom 3 Track Badges
    badges = [
        ("IBM TRACK", "6 Bob MCP Servers + watsonx", (5, 74, 218)),
        ("GOOGLE CLOUD", "Gemini 3.6 Flash + Vertex AI", (66, 133, 244)),
        ("CONFLUENT", "Real-Time Kafka Streaming", (16, 185, 129)),
    ]
    x_start = 320
    for title, subtitle, col in badges:
        draw.rounded_rectangle([(x_start, 740), (x_start + 380, 840)], radius=12, fill=(15, 23, 42), outline=col, width=2)
        draw.text((x_start + 190, 770), title, font=get_font(FONT_BOLD, 22), fill=col, anchor="mm")
        draw.text((x_start + 190, 805), subtitle, font=get_font(FONT_REGULAR, 17), fill=(203, 213, 225), anchor="mm")
        x_start += 450

    img.save(OUTPUT_DIR / "intro_title.png")
    print("Created intro_title.png")

def create_problem_card():
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    draw_header_badges(draw, "THE PROBLEM", (239, 68, 68))

    draw.text((960, 140), "THE $50,000+ ON-SET RESHOOT CRISIS", font=get_font(FONT_BOLD, 48), fill=(255, 255, 255), anchor="mm")
    draw.text((960, 200), "Human script supervisors face impossible multi-camera digital shooting conditions", font=get_font(FONT_REGULAR, 24), fill=(148, 163, 184), anchor="mm")

    cards = [
        ("3-4 CAMERAS SIMULTANEOUS", '"With so much more to notate, multitasking is\nstretched to the limit across multi-camera setups."\n— Jayne-Anne Tenggren (Star Wars, 1917), Forbes', (225, 29, 72)),
        ("30:1 to 150:1 RATIOS", "A 2-hour movie produces 25 to 375 hours of raw takes.\nContinuity slips through fatigued human memory.", (245, 158, 11)),
        ("$50,000 - $100,000 RESHOOTS", "When errors are discovered in post-production, pickup\nreshoot days can bankrupt indie and studio budgets.", (239, 68, 68)),
    ]
    x_start = 120
    for title, desc, col in cards:
        draw.rounded_rectangle([(x_start, 300), (x_start + 520, 680)], radius=16, fill=(15, 23, 42), outline=col, width=2)
        draw.rectangle([(x_start + 30, 340), (x_start + 100, 344)], fill=col)
        draw.text((x_start + 40, 390), title, font=get_font(FONT_BOLD, 26), fill=(255, 255, 255))
        draw.text((x_start + 40, 480), desc, font=get_font(FONT_REGULAR, 20), fill=(203, 213, 225))
        x_start += 580

    # Bottom stat banner
    draw.rounded_rectangle([(120, 760), (1800, 920)], radius=16, fill=(24, 24, 37), outline=(99, 102, 241), width=2)
    draw.text((960, 810), "Existing tools track scripts & notes. Shadow Cut tracks continuity in live pixels.", font=get_font(FONT_BOLD, 30), fill=(248, 250, 252), anchor="mm")
    draw.text((960, 865), "Shadow Cut bridges this blind spot: from $50,000 reshoots down to $7.00 per movie (7,000x ROI).", font=get_font(FONT_REGULAR, 24), fill=(129, 140, 248), anchor="mm")

    img.save(OUTPUT_DIR / "problem_card.png")
    print("Created problem_card.png")

def create_solution_card():
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    draw_header_badges(draw, "THE SOLUTION", (59, 130, 246))

    draw.text((960, 130), "SHADOW CUT: AUTONOMOUS ON-SET CONTINUITY", font=get_font(FONT_BOLD, 46), fill=(255, 255, 255), anchor="mm")
    draw.text((960, 185), '"The director still directs. The Shadow just remembers."', font=get_font(FONT_BOLD, 26), fill=(245, 158, 11), anchor="mm")

    import textwrap
    steps = [
        ("1. INGEST SCRIPT", "Before Day 1, Gemini Pro decomposes the screenplay into a structured Plot Graph of critical props and setup/payoff links.", (59, 130, 246)),
        ("2. WATCH TAKES", "As DIT uploads H.264 proxies, local YOLO-World and Gemini 3.5 Flash-Lite verify spatial consistency in under 15 seconds.", (16, 185, 129)),
        ("3. DETECT ANOMALIES", "Physical anomalies are checked against authentic screenplay requirements with non-dampening confidence scores.", (168, 85, 247)),
        ("4. DIRECTOR TRIAGE", "The director receives objective evidence with 3 actions: [Retake Take], [Accept Risk], or [Dismiss]. AI never dictates art.", (245, 158, 11)),
    ]
    x_start = 100
    for title, desc, col in steps:
        draw.rounded_rectangle([(x_start, 260), (x_start + 400, 720)], radius=16, fill=(15, 23, 42), outline=col, width=2)
        draw.rectangle([(x_start + 25, 295), (x_start + 85, 299)], fill=col)
        draw.text((x_start + 30, 330), title, font=get_font(FONT_BOLD, 22), fill=col)
        wrapped_desc = textwrap.fill(desc, width=30)
        draw.text((x_start + 30, 400), wrapped_desc, font=get_font(FONT_REGULAR, 19), fill=(203, 213, 225))
        x_start += 430

    # Bottom stat
    draw.rounded_rectangle([(100, 780), (1820, 930)], radius=16, fill=(24, 24, 37), outline=(16, 185, 129), width=2)
    draw.text((960, 830), "From $50,000 reshoots down to $7.00 per feature film.", font=get_font(FONT_BOLD, 30), fill=(248, 250, 252), anchor="mm")
    draw.text((960, 885), "7,000x Return on Investment — Built with Google Gemini, IBM Bob MCP Servers, & Confluent.", font=get_font(FONT_REGULAR, 22), fill=(52, 211, 153), anchor="mm")

    img.save(OUTPUT_DIR / "solution_card.png")
    print("Created solution_card.png")

def create_architecture_card():
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    draw_header_badges(draw, "SYSTEM ARCHITECTURE", (16, 185, 129))

    draw.text((960, 130), "MULTI-TIER AGENTIC CASCADE & CONFIDENCE ENGINE", font=get_font(FONT_BOLD, 46), fill=(255, 255, 255), anchor="mm")
    draw.text((960, 185), "Pre-computed Plot Knowledge Graph + Non-Dampening Confidence Gating", font=get_font(FONT_REGULAR, 22), fill=(148, 163, 184), anchor="mm")

    tiers = [
        ("TIER 1: YOLO-WORLD", "$0.00 / TAKE (LOCAL CPU/GPU)", "Real-time edge spatial tracking\nBounding boxes of script vocabulary\nZero cloud latency on DIT laptop", (16, 185, 129)),
        ("TIER 2: GEMINI 3.5 FLASH-LITE", "~$0.002 / TAKE (GOOGLE CLOUD)", "Multimodal video anomaly validation\nScript-to-pixel contextual checking\nTranscribes audio & director cues", (59, 130, 246)),
        ("TIER 3: GEMINI 3.1 PRO PREVIEW", "~$0.10 / ESCALATION (RARE)", "Complex cross-scene narrative logic\nTriggered only if confidence < 70%\nand prop is plot-CRITICAL", (168, 85, 247)),
    ]
    x_start = 120
    for title, cost, desc, col in tiers:
        draw.rounded_rectangle([(x_start, 260), (x_start + 520, 600)], radius=16, fill=(15, 23, 42), outline=col, width=2)
        draw.text((x_start + 35, 300), title, font=get_font(FONT_BOLD, 24), fill=col)
        draw.rounded_rectangle([(x_start + 35, 345), (x_start + 360, 385)], radius=8, fill=(30, 41, 59))
        draw.text((x_start + 45, 355), cost, font=get_font(FONT_BOLD, 15), fill=(241, 245, 249))
        draw.text((x_start + 35, 430), desc, font=get_font(FONT_REGULAR, 20), fill=(203, 213, 225))
        x_start += 580

    # Bottom formula box
    draw.rounded_rectangle([(120, 660), (1800, 940)], radius=16, fill=(24, 24, 37), outline=(51, 65, 85), width=2)
    draw.text((200, 710), "CONFIDENCE FORMULA & GATING:", font=get_font(FONT_BOLD, 24), fill=(245, 158, 11))
    draw.text((200, 760), "TechnicalConfidence = EvidenceScore × HistoryWeight × DetectionTrust", font=get_font(FONT_MONO, 26), fill=(56, 189, 248))
    draw.text((200, 820), "• PlotWeight is a strict DECISION GATE (CRITICAL / IMPORTANT / INCIDENTAL) — never a dampener", font=get_font(FONT_REGULAR, 20), fill=(226, 232, 240))
    draw.text((200, 860), "• Confidence ≥ 85% + CRITICAL  → PUSH ALERT to Director Command Center | < 70% → SILENT LOG in Memory", font=get_font(FONT_REGULAR, 20), fill=(226, 232, 240))

    img.save(OUTPUT_DIR / "architecture_card.png")
    print("Created architecture_card.png")

def create_bob_layout_bg():
    # 1920x1080 canvas for Bob screen recording
    # Left side: 1050x1080 for scaled video. Right side: 870x1080 info panel.
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)

    # Right side background
    draw.rectangle([(1060, 0), (1920, 1080)], fill=(15, 23, 42))
    draw.line([(1060, 0), (1060, 1080)], fill=(51, 65, 85), width=2)

    # Right side content
    draw.rounded_rectangle([(1100, 50), (1450, 95)], radius=12, fill=(5, 74, 218))
    draw.text((1125, 62), "IBM BOB INTEGRATION", font=get_font(FONT_BOLD, 20), fill=(255, 255, 255))

    draw.text((1100, 130), "RUNTIME NERVOUS SYSTEM", font=get_font(FONT_BOLD, 36), fill=(255, 255, 255))
    draw.text((1100, 180), "Bob generated our complete agentic infrastructure:", font=get_font(FONT_REGULAR, 20), fill=(148, 163, 184))

    items = [
        ("6 MCP SERVERS", "shadow_cut/mcp_servers/\nscript_parser, analyze_take, check_continuity,\nflag_alert, query_memory, generate_report", (59, 130, 246)),
        ("31 STRICT PYDANTIC SCHEMAS", "shadow_cut/models/schemas.py\nZero Dict[str, Any] — 100% strict enterprise types", (16, 185, 129)),
        ("777-LINE WATSONX SPEC", "shadow_cut/data/shadow_cut_orchestrate.yaml\nExposes all tools as native watsonx skills", (168, 85, 247)),
        ("CONFLUENT KAFKA CONSUMER", "shadow_cut/stream/confluent_consumer.py\nReal-time event streaming with fallback queue", (245, 158, 11)),
        ("CINEMATIC NEXT.JS 14 UI", "ui/components/\nModular dark-mode Command Center", (236, 72, 153)),
    ]
    y = 230
    for title, desc, col in items:
        draw.rounded_rectangle([(1100, y), (1880, y + 130)], radius=12, fill=(24, 24, 37), outline=col, width=1)
        draw.text((1130, y + 18), f"+  {title}", font=get_font(FONT_BOLD, 22), fill=col)
        draw.text((1130, y + 55), desc, font=get_font(FONT_REGULAR, 17), fill=(203, 213, 225))
        y += 155

    img.save(OUTPUT_DIR / "bob_layout_bg.png")
    print("Created bob_layout_bg.png")

def create_audit_title():
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    draw_header_badges(draw, "THE HERO BENCHMARK", (245, 158, 11))

    draw.text((960, 150), "20-MINUTE CONTINUOUS CINEMA AUDIT", font=get_font(FONT_BOLD, 48), fill=(255, 255, 255), anchor="mm")
    draw.text((960, 215), "George A. Romero's Night of the Living Dead (1968) · 142 Cuts Audited Against Authentic Screenplay", font=get_font(FONT_REGULAR, 24), fill=(148, 163, 184), anchor="mm")

    stats = [
        ("142", "Cuts Audited", (59, 130, 246)),
        ("1", "Critical Retake", (239, 68, 68)),
        ("2", "Director Reviews", (245, 158, 11)),
        ("99.2%", "Script Compliance", (16, 185, 129)),
    ]
    x_start = 160
    for num, label, col in stats:
        draw.rounded_rectangle([(x_start, 300), (x_start + 360, 480)], radius=16, fill=(15, 23, 42), outline=col, width=2)
        draw.text((x_start + 180, 370), num, font=get_font(FONT_BOLD, 64), fill=col, anchor="mm")
        draw.text((x_start + 180, 435), label, font=get_font(FONT_REGULAR, 22), fill=(241, 245, 249), anchor="mm")
        x_start += 410

    # Summary box
    draw.rounded_rectangle([(160, 550), (1760, 920)], radius=16, fill=(24, 24, 37), outline=(51, 65, 85), width=2)
    draw.text((220, 600), "REAL HISTORICAL CONTINUITY BREAKS DISCOVERED:", font=get_font(FONT_BOLD, 26), fill=(255, 255, 255))
    findings = [
        ("37:08", "Set Construction: Visible carpenter measurements & 'UPPER RIGHT CORNER' on barricade lumber", "RETAKE REQUIRED (100%)", (239, 68, 68)),
        ("07:58", "Prop Displacement: Charcoal lighter fluid canister jumps from hearth to floor across cuts", "DIRECTOR REVIEW (95%)", (245, 158, 11)),
        ("13:25", "Actor Staging Jump: Winchester repeating rifle shifts from vertical upright to horizontal across lap", "LOG ONLY (90%)", (148, 163, 184)),
        ("00:45", "Script Deviation: Duane Jones rips table apart bare-handed vs scripted iron tire iron & hammer", "ACCEPT RISK (91%)", (16, 185, 129)),
    ]
    y = 660
    for time_str, text, badge_str, b_col in findings:
        draw.rounded_rectangle([(220, y - 5), (320, y + 35)], radius=6, fill=(30, 41, 59))
        draw.text((235, y + 5), time_str, font=get_font(FONT_BOLD, 18), fill=(56, 189, 248))
        draw.text((345, y + 5), text, font=get_font(FONT_REGULAR, 20), fill=(226, 232, 240))
        draw.rounded_rectangle([(1450, y - 5), (1700, y + 35)], radius=6, fill=b_col)
        draw.text((1465, y + 5), badge_str, font=get_font(FONT_BOLD, 16), fill=(255, 255, 255))
        y += 65

    img.save(OUTPUT_DIR / "audit_title.png")
    print("Created audit_title.png")

def create_evidence_card(filename, title, subtitle, frame_a_path, frame_b_path, badge_text, badge_color, action_text, impact_text):
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    draw_header_badges(draw, "FORENSIC EVIDENCE", badge_color)

    # Title & Badge
    draw.text((60, 110), title, font=get_font(FONT_BOLD, 36), fill=(255, 255, 255))
    draw.text((60, 160), subtitle, font=get_font(FONT_REGULAR, 22), fill=(148, 163, 184))

    # Badge top right
    draw.rounded_rectangle([(1450, 95), (1860, 155)], radius=12, fill=badge_color)
    draw.text((1655, 125), badge_text, font=get_font(FONT_BOLD, 22), fill=(255, 255, 255), anchor="mm")

    # Load and paste frames
    if frame_a_path and Path(frame_a_path).exists():
        fa = Image.open(frame_a_path).convert("RGB")
        fa = fa.resize((860, 540))
        img.paste(fa, (60, 220))
        draw.rectangle([(60, 220), (920, 760)], outline=(51, 65, 85), width=2)
        draw.rectangle([(60, 220), (320, 260)], fill=(15, 23, 42))
        draw.text((75, 230), "SHOT A / REFERENCE", font=get_font(FONT_BOLD, 18), fill=(56, 189, 248))

    if frame_b_path and Path(frame_b_path).exists():
        fb = Image.open(frame_b_path).convert("RGB")
        fb = fb.resize((860, 540))
        img.paste(fb, (1000, 220))
        draw.rectangle([(1000, 220), (1860, 760)], outline=(51, 65, 85), width=2)
        draw.rectangle([(1000, 220), (1340, 260)], fill=(15, 23, 42))
        draw.text((1015, 230), "SHOT B / ANOMALY DETECTED", font=get_font(FONT_BOLD, 18), fill=(239, 68, 68))

    # Bottom action & impact card
    draw.rounded_rectangle([(60, 800), (1860, 1000)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.text((100, 830), "DIRECTOR ACTION:", font=get_font(FONT_BOLD, 22), fill=(245, 158, 11))
    draw.text((340, 830), action_text, font=get_font(FONT_BOLD, 22), fill=(255, 255, 255))

    draw.text((100, 890), "FORENSIC IMPACT:", font=get_font(FONT_BOLD, 22), fill=(56, 189, 248))
    draw.text((340, 890), impact_text, font=get_font(FONT_REGULAR, 22), fill=(226, 232, 240))

    img.save(OUTPUT_DIR / filename)
    print(f"Created {filename}")

def create_outro_card():
    img = Image.new("RGBA", (1920, 1080), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(60, 60), (1860, 1020)], outline=(30, 41, 59), width=2)

    draw.text((960, 220), "SHADOW CUT", font=get_font(FONT_BOLD, 84), fill=(255, 255, 255), anchor="mm")
    draw.text((960, 310), '"The director still directs. The Shadow just remembers."', font=get_font(FONT_BOLD, 36), fill=(245, 158, 11), anchor="mm")

    # Metrics banner
    draw.rounded_rectangle([(320, 400), (1600, 520)], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text((500, 460), "$7.00 / MOVIE", font=get_font(FONT_BOLD, 36), fill=(16, 185, 129), anchor="mm")
    draw.text((960, 460), "PREVENTS $50,000+ RESHOOTS", font=get_font(FONT_BOLD, 30), fill=(255, 255, 255), anchor="mm")
    draw.text((1420, 460), "7,000x ROI", font=get_font(FONT_BOLD, 36), fill=(16, 185, 129), anchor="mm")

    # Links card
    draw.rounded_rectangle([(320, 570), (1600, 870)], radius=16, fill=(24, 24, 37), outline=(51, 65, 85), width=2)
    draw.text((380, 630), "LIVE CLOUD RUN API:", font=get_font(FONT_BOLD, 24), fill=(56, 189, 248))
    draw.text((380, 675), "https://shadow-cut-api-713353926846.us-central1.run.app", font=get_font(FONT_MONO, 24), fill=(241, 245, 249))

    draw.text((380, 750), "GITHUB REPOSITORY:", font=get_font(FONT_BOLD, 24), fill=(168, 85, 247))
    draw.text((380, 795), "https://github.com/patriceai-code/shadow-cut", font=get_font(FONT_MONO, 24), fill=(241, 245, 249))

    draw.text((960, 940), "Built for Agentic Cinema Hackathon 2026 — IBM Track", font=get_font(FONT_REGULAR, 22), fill=(148, 163, 184), anchor="mm")

    img.save(OUTPUT_DIR / "outro_card.png")
    print("Created outro_card.png")

if __name__ == "__main__":
    create_intro_title()
    create_problem_card()
    create_solution_card()
    create_architecture_card()
    create_bob_layout_bg()
    create_audit_title()

    # Evidence Cards
    frames_dir = Path("ui/public/evidence_frames")
    create_evidence_card(
        "evidence_1_barricade.png",
        "Set Construction Anomaly: Barricade Lumber Marking",
        "Timestamp: 37:08 (Farmhouse Siege) · Plot Weight: CRITICAL",
        frames_dir / "03_set_door_barricade_wide_0230.jpg",
        frames_dir / "03_set_door_barricade_wide_0230.jpg",
        "RETAKE REQUIRED (99%)",
        (239, 68, 68),
        "[Retake Take] — Strike take and replace marked timber before exterior wrap",
        "Visible pencil carpentry measurements and 'UPPER RIGHT CORNER' facing the lens."
    )

    create_evidence_card(
        "evidence_2_lighter_fluid.png",
        "Prop Continuity: Charcoal Lighter Canister Displacement",
        "Timestamp: 07:58 → 08:15 (Living Room Reverse Setup) · Plot Weight: IMPORTANT",
        frames_dir / "01_prop_lighter_fluid_shotA_0758.jpg",
        frames_dir / "01_prop_lighter_fluid_shotB_0815.jpg",
        "DIRECTOR REVIEW (95%)",
        (245, 158, 11),
        "[Director Review] — Check coverage or accept cutaway edit",
        "Canister is upright by hearth in Shot A, then abruptly rests on floor by chair in Shot B."
    )

    create_evidence_card(
        "evidence_3_rifle.png",
        "Actor / Prop Staging: Winchester Repeating Rifle Orientation",
        "Timestamp: 13:25 → 13:35 (Ben & Barbra Dialogue) · Plot Weight: INCIDENTAL",
        frames_dir / "02_prop_rifle_shotA_vertical_1325.jpg",
        frames_dir / "02_prop_rifle_shotB_horizontal_1335.jpg",
        "LOG ONLY (90%)",
        (100, 116, 139),
        "[Log Only] — Recorded to Firestore memory; no push alert dispatched",
        "Rifle rests vertically against doorframe, then horizontally across lap between cuts."
    )

    create_evidence_card(
        "evidence_4_table_deviation.png",
        "Screenplay Deviation: Table Disassembly Technique",
        "Timestamp: 00:45 · Screenplay vs Performance · Script Compliance: 99.2%",
        frames_dir / "04_script_deviation_table_bare_hands_0045.jpg",
        frames_dir / "04_script_deviation_table_bare_hands_0045.jpg",
        "ACCEPT RISK (91%)",
        (16, 185, 129),
        "[Accept Risk] — Director approves actor improvisation; logged to production memory",
        "Script called for tire iron/hammer; Duane Jones used bare hands with intense physical struggle."
    )

    create_outro_card()
    print("All graphic cards generated successfully!")
