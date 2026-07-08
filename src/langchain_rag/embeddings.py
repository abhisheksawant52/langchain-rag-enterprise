"""Embedding provider abstraction.

Wraps LangChain embedding integrations so the rest of the application depends
on a single factory rather than concrete provider classes.
"""

from __future__ import annotations

from typing import Any

from langchain_rag.config import Settings, get_settings
from langchain_rag.logging_config import get_logger

logger = get_logger(__name__)


def build_embeddings(settings: Settings | None = None) -> Any:
    """Build an embeddings client from settings.

    Uses ``langchain_openai.OpenAIEmbeddings``. The object is constructed but
    not invoked, so no network call is made at import time.

    Args:
        settings: Optional settings override.

    Returns:
        A LangChain embeddings instance.
    """
    settings = settings or get_settings()
    from langchain_openai import OpenAIEmbeddings

    logger.debug("Building embeddings with model %s", settings.embedding_model)
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
