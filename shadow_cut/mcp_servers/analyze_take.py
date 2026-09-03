# mcp_servers/analyze_take.py
"""
Analyze take tool for Shadow Cut.
If using IBM Bob / watsonx Orchestrate, Bob will generate the @tool decorator.
For local development and testing, defined as a plain typed function.
"""
from shadow_cut.core.bridge import FlashLiteBridge
from shadow_cut.config.settings import get_settings

def analyze_take(video_path: str, yolo_math: dict, scene_context: dict, script_summary: str = "") -> dict:
    """Validate YOLO anomalies with script context."""
    settings = get_settings()
    bridge = FlashLiteBridge(api_key=settings.gemini_api_key)
    return bridge.validate_take(video_path, yolo_math, scene_context, script_summary)
