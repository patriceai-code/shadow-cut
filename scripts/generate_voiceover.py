"""
Generate broadcast-quality neural voiceover narration for the Shadow Cut demo video using edge-tts.
Voice: en-US-ChristopherNeural (authoritative, clear, professional documentary tone)
"""
import asyncio
from pathlib import Path
import edge_tts

AUDIO_DIR = Path("demo_production/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "en-US-ChristopherNeural"

SCRIPTS = {
    "act1_hook": (
        "On a film set, missing a single continuity error can cost a production upwards of "
        "fifty to one hundred thousand dollars in pickup reshoots. With multi-camera shoots and "
        "thirty-to-one shooting ratios, human script supervisors are overwhelmed tracking thousands "
        "of props, wardrobe states, and lighting setups by hand. "
        "Meet Shadow Cut — the autonomous on-set AI script supervisor that watches every take as it's "
        "filmed, grounds visual evidence against the authentic shooting screenplay, and alerts the director "
        "while the cast and crew are still on set."
    ),
    "act2_architecture_bob": (
        "Shadow Cut uses a multi-tier agentic cascade. Tier 1 runs local YOLO-World spatial tracking on "
        "edge hardware for real-time prop detection. Tier 2 streams take proxies to Gemini 3.5 Flash-Lite "
        "for native multimodal reasoning against the script. "
        "For the Agentic Cinema IBM Track, IBM Bob served as our runtime nervous system. Bob generated all six "
        "Model Context Protocol servers in Python, established thirty-one strict Pydantic v2 schemas with zero dynamic "
        "dictionaries, and built a 777-line OpenAPI specification for IBM watsonx Orchestrate. "
        "In addition, Bob implemented real-time Confluent Kafka streaming with an automated fallback webhook."
    ),
    "act3_hero_audit": (
        "To prove Shadow Cut on genuine cinema, we conducted an exhaustive twenty-minute audit of 142 cuts "
        "from George A. Romero's 1968 classic Night of the Living Dead, cross-referenced against the original shooting screenplay. "
        "Shadow Cut surfaced four authentic historical continuity breaks: "
        "First, at thirty-seven minutes, a Critical Retake Alert caught visible pencil carpentry measurements and "
        "'Upper Right Corner' written on the raw barricade lumber facing the lens. "
        "Second, a lighter fluid canister jump between the fireplace hearth and chair across reverse cuts. "
        "Third, a staging shift of the repeating rifle. "
        "And fourth, a script deviation where Duane Jones ripped an oak table apart bare-handed instead of the scripted tire iron. "
        "Under our Director Autonomy Principle, the AI never dictates art: the filmmaker retains full control to Retake, Dismiss, or Accept Risk."
    ),
    "act4_command_center": (
        "On set, directors monitor production through our dark-room Next.js Command Center. "
        "The live dashboard tracks audited cuts, critical retake alerts, and a ninety-nine-point-two percent script compliance score. "
        "Filmmakers inspect side-by-side frame comparisons, review screenplay deviations, and interact directly with Shadow Memory "
        "powered by Gemini 3.6 Flash. "
        "The platform is deployed live on Google Cloud Run, delivering real-time continuity protection for just seven dollars per movie — "
        "preventing fifty-thousand-dollar reshoots with a 7,000x return on investment. "
        "Shadow Cut: The director still directs. The Shadow just remembers."
    )
}

async def generate_all():
    print(f"Generating voiceover files using {VOICE}...")
    for key, text in SCRIPTS.items():
        out_path = AUDIO_DIR / f"{key}.mp3"
        print(f"Generating {out_path.name}...")
        communicate = edge_tts.Communicate(text, VOICE, rate="+3%")
        await communicate.save(str(out_path))
        print(f"  [OK] Saved {out_path.name}")

if __name__ == "__main__":
    asyncio.run(generate_all())
