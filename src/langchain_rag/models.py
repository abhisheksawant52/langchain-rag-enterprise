"""Pydantic request/response models for the HTTP API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single conversation message."""

    role: Literal["user", "assistant", "system"] = Field(
        description="Author role of the message."
    )
    content: str = Field(min_length=1, description="Message text content.")


class ChatRequest(BaseModel):
    """Request body for the ``/chat`` endpoint."""

    session_id: str = Field(
        default="default",
        min_length=1,
        description="Conversation session identifier used to key memory.",
    )
    message: str = Field(min_length=1, description="User message to answer.")


class SourceDocument(BaseModel):
    """A retrieved document surfaced as an answer citation."""

    content: str = Field(description="Retrieved chunk content.")
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Arbitrary document metadata."
    )


class ChatResponse(BaseModel):
    """Response body for the ``/chat`` endpoint."""

    session_id: str = Field(description="Echoed conversation session identifier.")
    answer: str = Field(description="Generated assistant answer.")
    sources: list[SourceDocument] = Field(
        default_factory=list, description="Documents used to ground the answer."
    )


class QueryRequest(BaseModel):
    """Request body for the stateless ``/query`` endpoint."""

    question: str = Field(min_length=1, description="Question to answer.")
    top_k: int | None = Field(
        default=None, ge=1, description="Optional override for retrieval depth."
    )


class QueryResponse(BaseModel):
    """Response body for the ``/query`` endpoint."""

    question: str = Field(description="Echoed question.")
    answer: str = Field(description="Generated answer.")
    sources: list[SourceDocument] = Field(
        default_factory=list, description="Documents used to ground the answer."
    )


class IngestRequest(BaseModel):
    """Request body for the ``/ingest`` endpoint."""

    documents: list[str] = Field(
        min_length=1, description="Raw text documents to embed and index."
    )
    metadata: list[dict[str, str]] | None = Field(
        default=None, description="Optional per-document metadata."
    )


class IngestResponse(BaseModel):
    """Response body for the ``/ingest`` endpoint."""

    ingested: int = Field(ge=0, description="Number of documents indexed.")
    collection: str = Field(description="Target vector store collection.")


class HealthStatus(BaseModel):
    """Health / readiness probe response."""

    status: Literal["ok", "degraded", "error"] = Field(description="Overall status.")
    service: str = Field(description="Service name.")
    version: str = Field(description="Running application version.")
