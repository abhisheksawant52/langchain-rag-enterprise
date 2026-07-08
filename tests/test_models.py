"""Tests for pydantic request/response models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from langchain_rag.models import (
    ChatRequest,
    IngestRequest,
    Message,
    QueryRequest,
)


def test_chat_request_defaults_session() -> None:
    request = ChatRequest(message="hello")
    assert request.session_id == "default"
    assert request.message == "hello"


def test_chat_request_rejects_empty_message() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="")


def test_message_rejects_invalid_role() -> None:
    with pytest.raises(ValidationError):
        Message(role="robot", content="hi")


def test_query_request_top_k_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        QueryRequest(question="q", top_k=0)


def test_ingest_request_requires_documents() -> None:
    with pytest.raises(ValidationError):
        IngestRequest(documents=[])

    valid = IngestRequest(documents=["doc one"])
    assert valid.documents == ["doc one"]
