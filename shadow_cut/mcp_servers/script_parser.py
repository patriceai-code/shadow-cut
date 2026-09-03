# mcp_servers/script_parser.py
"""
Script parser tool for Shadow Cut.
If using IBM Bob / watsonx Orchestrate, Bob will generate the @tool decorator.
For local development and testing, defined as a plain typed function.
"""
from shadow_cut.core.plot_graph import PlotGraphBuilder
from shadow_cut.config.settings import get_settings

def parse_script(script_text: str, format: str = "txt") -> dict:
    """Parse film script into Plot Knowledge Graph."""
    settings = get_settings()
    builder = PlotGraphBuilder(api_key=settings.gemini_api_key)
    return builder.parse_script(script_text)
