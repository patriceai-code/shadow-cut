"""
Generate natural, human-sounding neural voiceover per visual beat using en-US-AndrewNeural.
Rate: +5% (natural conversational cadence).
Target duration: ~2:35 to 2:45 (comfortably under the 3-minute Devpost ceiling).
"""
import asyncio
import json
import subprocess
from pathlib import Path
import edge_tts

AUDIO_DIR = Path("demo_production/audio_synced")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "en-US-AndrewNeural"

BEATS = [
    # --- ACT 1: THE HOOK ---
    {
        "id": "act1_b1_title",
        "act": 1,
        "visual_type": "still",
        "visual_file": "intro_title.png",
        "text": "On a film set, missing a single continuity error can cost upwards of fifty to one hundred thousand dollars in pickup reshoots."
    },
    {
        "id": "act1_b2_movie",
        "act": 1,
        "visual_type": "movie_clip",
        "visual_file": "farmhouse_scene.mp4",
        "text": "With multi-camera shoots and thirty-to-one shooting ratios, human script supervisors are overwhelmed tracking thousands of props, wardrobe states, and lighting setups by hand."
    },
    {
        "id": "act1_b3_crisis",
        "act": 1,
        "visual_type": "still",
        "visual_file": "problem_card.png",
        "text": "When continuity errors are caught in post-production, reshoots can easily derail a production budget."
    },
    {
        "id": "act1_b4_solution",
        "act": 1,
        "visual_type": "still",
        "visual_file": "solution_card.png",
        "text": "Meet Shadow Cut — the autonomous AI script supervisor that watches every take as it's filmed, grounds visual evidence against the authentic screenplay, and alerts the director while still on set."
    },

    # --- ACT 2: ARCHITECTURE & IBM BOB ---
    {
        "id": "act2_b1_architecture",
        "act": 2,
        "visual_type": "still",
        "visual_file": "architecture_card.png",
        "text": "Shadow Cut uses a multi-tier agentic cascade: Tier 1 runs local Yo-low World spatial tracking on edge hardware, while Tier 2 streams take proxies to Gemini 3.5 Flash Lite for native multimodal reasoning."
    },
    {
        "id": "act2_b2_bob_intro",
        "act": 2,
        "visual_type": "bob_recording",
        "visual_file": "bob_layout_bg.png",
        "ss": 5.0,
        "text": "For the Agentic Cinema IBM Track, IBM Bob served as our runtime nervous system."
    },
    {
        "id": "act2_b3_bob_servers",
        "act": 2,
        "visual_type": "bob_recording",
        "visual_file": "bob_layout_bg.png",
        "ss": 20.0,
        "text": "Bob generated all six Model Context Protocol servers in Python, and established thirty-one strict Pydantic schemas with zero dynamic dictionaries."
    },
    {
        "id": "act2_b4_watsonx_confluent",
        "act": 2,
        "visual_type": "bob_recording",
        "visual_file": "bob_layout_bg.png",
        "ss": 38.0,
        "text": "Bob built our 777-line OpenAPI specification for IBM Watson X Orchestrate, and implemented real-time Confluent Kafka streaming with an automated fallback webhook."
    },

    # --- ACT 3: THE HERO AUDIT ---
    {
        "id": "act3_b1_audit_title",
        "act": 3,
        "visual_type": "still",
        "visual_file": "audit_title.png",
        "text": "To prove Shadow Cut on genuine cinema, we conducted a twenty-minute audit of 142 cuts from George Romero's 1968 classic Night of the Living Dead, cross-referenced against the authentic screenplay."
    },
    {
        "id": "act3_b2_barricade",
        "act": 3,
        "visual_type": "still",
        "visual_file": "evidence_1_barricade.png",
        "text": "First, at thirty-seven minutes, a Critical Retake Alert caught visible pencil carpentry measurements and 'Upper Right Corner' written on the raw barricade lumber facing the lens."
    },
    {
        "id": "act3_b3_lighter",
        "act": 3,
        "visual_type": "still",
        "visual_file": "evidence_2_lighter_fluid.png",
        "text": "Second, a lighter fluid canister jump between the fireplace hearth and chair across reverse cuts, flagged for Director Review."
    },
    {
        "id": "act3_b4_rifle",
        "act": 3,
        "visual_type": "still",
        "visual_file": "evidence_3_rifle.png",
        "text": "Third, an actor staging jump where the repeating rifle shifts from vertical against the doorway to horizontal across Ben's lap, logged silently in memory."
    },
    {
        "id": "act3_b5_table",
        "act": 3,
        "visual_type": "still",
        "visual_file": "evidence_4_table_deviation.png",
        "text": "And fourth, a performance deviation where Duane Jones ripped an oak table apart bare-handed. Under our Director Autonomy Principle, the director can Retake, Dismiss, or Accept Risk on actor improvisation."
    },

    # --- ACT 4: COMMAND CENTER & OUTRO ---
    {
        "id": "act4_b1_dashboard",
        "act": 4,
        "visual_type": "ui_segment",
        "ss": 0.5,
        "text": "On set, directors monitor production through our dark-room Next.js Command Center, tracking audited cuts, critical retake alerts, and a ninety-nine-point-two percent script compliance score."
    },
    {
        "id": "act4_b2_alerts",
        "act": 4,
        "visual_type": "ui_segment",
        "ss": 16.5,
        "text": "Filmmakers inspect side-by-side frame comparisons on flagged cuts, and review screenplay performance deviations."
    },
    {
        "id": "act4_b3_chat",
        "act": 4,
        "visual_type": "ui_segment",
        "ss": 23.0,
        "text": "They can query Shadow Memory in natural language, retrieving grounded timestamps, prop states, and script rules in real time."
    },
    {
        "id": "act4_b4_trust_report",
        "act": 4,
        "visual_type": "ui_segment",
        "ss": 31.0,
        "text": "Deployed live on Google Cloud Run, Shadow Cut provides real-time continuity protection for just seven dollars per movie — preventing fifty-thousand-dollar reshoots with a seven-thousand-X return on investment."
    },
    {
        "id": "act4_b5_outro",
        "act": 4,
        "visual_type": "still",
        "visual_file": "outro_card.png",
        "text": "Shadow Cut: The director still directs. The Shadow just remembers.",
        "extra_padding": 2.1
    }
]

def get_duration(audio_file):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def generate_beat_audio():
    print(f"Generating human natural voiceovers with {VOICE} at +4% rate...")
    manifest = []
    total_dur = 0.0

    for b in BEATS:
        out_file = AUDIO_DIR / f"{b['id']}.mp3"
        print(f"Generating [{b['id']}]...")
        comm = edge_tts.Communicate(b['text'], VOICE, rate="+6%")
        await comm.save(str(out_file))

        dur = get_duration(out_file)
        extra = b.get("extra_padding", 0.15)
        dur_padded = round(dur + extra, 3)
        total_dur += dur_padded

        b_data = dict(b)
        b_data["audio_file"] = str(out_file)
        b_data["raw_duration"] = dur
        b_data["duration"] = dur_padded
        manifest.append(b_data)
        print(f"  [OK] {b['id']} -> {dur:.2f}s (padded: {dur_padded:.2f}s)")

    manifest_path = Path("demo_production/beat_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest saved to {manifest_path}")
    print(f"Total Video Duration will be: {total_dur:.2f} seconds ({int(total_dur // 60)}m {int(total_dur % 60)}s)")

if __name__ == "__main__":
    asyncio.run(generate_beat_audio())
