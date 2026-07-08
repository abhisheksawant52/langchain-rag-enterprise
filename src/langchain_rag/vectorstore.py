"""Vector store provider abstraction.

Provides a factory for constructing the backing vector store used for
similarity search. An in-memory FAISS store is used as the default provider so
the application can run without external infrastructure.
"""

from __future__ import annotations

from typing import Any

from langchain_rag.config import Settings, get_settings
from langchain_rag.embeddings import build_embeddings
from langchain_rag.logging_config import get_logger

logger = get_logger(__name__)


def build_vectorstore(
    settings: Settings | None = None,
    embeddings: Any | None = None,
    texts: list[str] | None = None,
) -> Any:
    """Build a FAISS-backed vector store.

    Args:
        settings: Optional settings override.
        embeddings: Optional pre-built embeddings client.
        texts: Optional seed texts to index at construction time.

    Returns:
        A LangChain ``VectorStore`` instance.
    """
    settings = settings or get_settings()
    embeddings = embeddings or build_embeddings(settings)

    from langchain_community.vectorstores import FAISS

    seed = texts or ["langchain-rag-enterprise bootstrap document"]
    logger.debug("Building FAISS vector store with %d seed docs", len(seed))
    return FAISS.from_texts(texts=seed, embedding=embeddings)


def add_documents(vectorstore: Any, texts: list[str], metadatas: list[dict] | None = None) -> int:
    """Add raw text documents to an existing vector store.

    Args:
        vectorstore: A LangChain vector store instance.
        texts: Text documents to embed and index.
        metadatas: Optional per-document metadata.

    Returns:
        The number of documents added.
    """
    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    return len(texts)
