"""Application configuration.

Settings are loaded from environment variables (prefixed ``LCRAG_``) or an
``.env`` file using ``pydantic-settings``. Access the cached singleton through
:func:`get_settings`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the RAG service.

    All values may be overridden via environment variables using the
    ``LCRAG_`` prefix, e.g. ``LCRAG_LLM_MODEL=gpt-4o``.
    """

    model_config = SettingsConfigDict(
        env_prefix="LCRAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(
        default="langchain-rag-enterprise",
        description="Human-readable application name.",
    )
    environment: str = Field(
        default="development",
        description="Deployment environment (development, staging, production).",
    )
    log_level: str = Field(
        default="INFO",
        description="Root logging level.",
    )
    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key. Optional; no default secret is shipped.",
    )
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="Embedding model identifier used to vectorise documents.",
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="Chat/completion model used to synthesise answers.",
    )
    vector_store_url: str = Field(
        default="http://localhost:6333",
        description="Connection URL for the backing vector store.",
    )
    top_k: int = Field(
        default=4,
        ge=1,
        description="Number of documents to retrieve per query.",
    )
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for the LLM.",
    )
    memory_window: int = Field(
        default=5,
        ge=1,
        description="Number of recent conversation turns to keep in memory.",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
