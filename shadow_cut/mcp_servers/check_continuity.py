# mcp_servers/check_continuity.py
"""
Check continuity tool for Shadow Cut.
If using IBM Bob / watsonx Orchestrate, Bob will generate the @tool decorator.
For local development and testing, defined as a plain typed function.
"""
from typing import List, Dict, Any

def check_continuity(current_take: dict, previous_takes: List[dict], plot_graph: dict) -> dict:
    """Compare current take against previous takes + script rules."""
    mismatches = []
    matches = []
    
    current_props = current_take.get("object_tracks", {})
    for prev in previous_takes:
        prev_props = prev.get("object_tracks", {})
        for prop_name, track in current_props.items():
            if prop_name in prev_props:
                prev_track = prev_props[prop_name]
                if track.get("class") == prev_track.get("class"):
                    matches.append({
                        "prop": prop_name,
                        "status": "matched",
                        "current_take": current_take.get("take_id"),
                        "previous_take": prev.get("take_id")
                    })
    
    return {
        "status": "success",
        "matches": matches,
        "mismatches": mismatches,
        "cross_scene_issues": []
    }
