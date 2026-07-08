"""Application service orchestrating the RAG chain and conversation memory."""

from __future__ import annotations

from typing import Any

from langchain_rag.config import Settings, get_settings
from langchain_rag.logging_config import get_logger
from langchain_rag.memory import WindowedConversationMemory
from langchain_rag.models import (
    ChatResponse,
    IngestResponse,
    QueryResponse,
    SourceDocument,
)

logger = get_logger(__name__)


class RagChatService:
    """Orchestrate retrieval, generation, and per-session memory.

    The chain and vector store are built lazily on first use so that
    constructing the service (and importing the module) never triggers network
    calls or requires credentials.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialise the service.

        Args:
            settings: Optional settings override.
        """
        self.settings = settings or get_settings()
        self._chain: Any | None = None
        self._vectorstore: Any | None = None
        self._sessions: dict[str, WindowedConversationMemory] = {}

    # -- lazy component builders -------------------------------------------

    def _get_vectorstore(self) -> Any:
        if self._vectorstore is None:
            from langchain_rag.vectorstore import build_vectorstore

            self._vectorstore = build_vectorstore(self.settings)
        return self._vectorstore

    def _get_chain(self) -> Any:
        if self._chain is None:
            from langchain_rag.chains import build_rag_chain
            from langchain_rag.retrievers import build_retriever

            retriever = build_retriever(self.settings, vectorstore=self._get_vectorstore())
            self._chain = build_rag_chain(self.settings, retriever=retriever)
        return self._chain

    def _memory_for(self, session_id: str) -> WindowedConversationMemory:
        if session_id not in self._sessions:
            self._sessions[session_id] = WindowedConversationMemory(
                window=self.settings.memory_window
            )
        return self._sessions[session_id]

    # -- public API --------------------------------------------------------

    def chat(self, session_id: str, message: str) -> ChatResponse:
        """Answer a message within a conversation session."""
        memory = self._memory_for(session_id)
        chain = self._get_chain()
        answer = chain.invoke(message)
        memory.add_turn(message, answer)
        logger.info("Handled chat turn for session %s", session_id)
        return ChatResponse(session_id=session_id, answer=answer, sources=[])

    def query(self, question: str, top_k: int | None = None) -> QueryResponse:
        """Answer a stateless question."""
        chain = self._get_chain()
        answer = chain.invoke(question)
        return QueryResponse(question=question, answer=answer, sources=[])

    def ingest(self, documents: list[str], metadata: list[dict] | None = None) -> IngestResponse:
        """Embed and index new documents into the vector store."""
        from langchain_rag.vectorstore import add_documents

        count = add_documents(self._get_vectorstore(), documents, metadata)
        logger.info("Ingested %d documents", count)
        return IngestResponse(ingested=count, collection=self.settings.app_name)

    def history(self, session_id: str) -> list[SourceDocument]:
        """Return the rendered conversation history for a session (debug aid)."""
        memory = self._memory_for(session_id)
        return [SourceDocument(content=m.content, metadata={"role": m.role}) for m in memory.messages()]
