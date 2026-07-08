"""Vector-store-backed retriever configuration."""

from __future__ import annotations

from typing import Any

from langchain_rag.config import Settings, get_settings
from langchain_rag.logging_config import get_logger
from langchain_rag.vectorstore import build_vectorstore

logger = get_logger(__name__)


def build_retriever(
    settings: Settings | None = None,
    vectorstore: Any | None = None,
    top_k: int | None = None,
) -> Any:
    """Build a similarity-search retriever from a vector store.

    Args:
        settings: Optional settings override.
        vectorstore: Optional pre-built vector store.
        top_k: Optional override for the number of documents to retrieve.

    Returns:
        A LangChain retriever configured for similarity search.
    """
    settings = settings or get_settings()
    vectorstore = vectorstore or build_vectorstore(settings)
    k = top_k or settings.top_k

    logger.debug("Building retriever with top_k=%d", k)
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
