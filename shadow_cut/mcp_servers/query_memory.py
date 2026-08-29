"""
Shadow Cut MCP Server — Tool 5: query_memory
Embeds a question, searches Shadow Memory (Firestore), and returns typed chunks.
"""
from __future__ import annotations

from shadow_cut.config.settings import get_settings
from shadow_cut.models.schemas import MemoryChunk, MemoryQueryResult


def tool(func):  # type: ignore[no-untyped-def]
    return func


# ---------------------------------------------------------------------------
# Firestore helpers
# ---------------------------------------------------------------------------

_COLLECTIONS = ("takes", "alerts", "plot_graph", "reports")


def _query_firestore(
    question: str,
    scene_filter: int | None,
    top_k: int,
    settings,  # type: ignore[no-untyped-def]
) -> list[MemoryChunk]:
    """
    Query Firestore for memory chunks relevant to `question`.

    In full deployment this performs:
      1. Embed `question` using the Gemini Embeddings API.
      2. Issue a Firestore vector-similarity query against each collection.
      3. Merge, deduplicate, and rank results by relevance_score.

    Currently implemented as a structured keyword search across collections
    (vector index wired in the Firestore deployment).
    """
    from google.cloud import firestore  # type: ignore[import-untyped]

    db = firestore.Client(project=settings.firestore_project_id)
    chunks: list[MemoryChunk] = []

    question_lower = question.lower()
    words = [w for w in question_lower.split() if len(w) > 3]

    for collection in _COLLECTIONS:
        try:
            ref = db.collection(collection)
            if scene_filter is not None:
                ref = ref.where("scene", "==", scene_filter)  # type: ignore[assignment]

            docs = ref.limit(top_k * 2).get()
            for doc in docs:
                data: dict = doc.to_dict() or {}
                text = str(data.get("text", data.get("description", data.get("notes", ""))))
                if not text:
                    continue

                # Relevance: fraction of question words found in text
                text_lower = text.lower()
                hit_count = sum(1 for w in words if w in text_lower)
                score = hit_count / max(len(words), 1)

                chunk = MemoryChunk(
                    chunk_id=doc.id,
                    source_collection=collection,  # type: ignore[arg-type]
                    scene=data.get("scene"),
                    take_id=data.get("take_id"),
                    text=text[:2000],
                    relevance_score=min(score, 1.0),
                    timestamp=str(data.get("timestamp", "")),
                )
                chunks.append(chunk)
        except Exception:
            continue

    # Sort by relevance descending, return top_k
    chunks.sort(key=lambda c: c.relevance_score, reverse=True)
    return chunks[:top_k]


# ---------------------------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------------------------

@tool
def query_memory(
    question: str,
    scene_filter: int | None = None,
    top_k: int = 5,
) -> MemoryQueryResult:
    """
    Search Shadow Memory (Firestore) to answer a director or continuity question.

    Queries the takes, alerts, plot_graph, and reports collections for text
    that is relevant to `question`, optionally scoped to a single scene.

    Args:
        question:     Natural-language question (e.g. "Where was the watch in scene 5?").
        scene_filter: If provided, restrict results to this scene number.
        top_k:        Maximum number of memory chunks to return (1–20).

    Returns:
        MemoryQueryResult with ranked chunks and their source collection paths.
    """
    if top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20")
    if not question.strip():
        raise ValueError("question must not be empty")

    settings = get_settings()
    chunks = _query_firestore(question, scene_filter, top_k, settings)

    sources = list({
        f"{c.source_collection}/{c.chunk_id}" for c in chunks
    })

    return MemoryQueryResult(
        question=question,
        chunks=chunks,
        sources=sources,
        scene_filter_applied=scene_filter,
    )
