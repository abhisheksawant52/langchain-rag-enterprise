"""langchain-rag-enterprise.

An enterprise-grade Retrieval-Augmented Generation (RAG) application built on
LangChain and served through FastAPI. The package wires together an embedding
provider, a vector store, retrieval-QA chains, and windowed conversational
memory behind a small HTTP API.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "get_settings",
    "Settings",
    "create_app",
    "RagChatService",
]

from langchain_rag.config import Settings, get_settings
from langchain_rag.main import create_app
from langchain_rag.service import RagChatService
