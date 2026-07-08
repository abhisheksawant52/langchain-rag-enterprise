"""FastAPI application exposing the RAG chat/query API."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends, FastAPI

from langchain_rag import __version__
from langchain_rag.config import Settings, get_settings
from langchain_rag.logging_config import configure_logging, get_logger
from langchain_rag.models import (
    ChatRequest,
    ChatResponse,
    HealthStatus,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)
from langchain_rag.service import RagChatService

logger = get_logger(__name__)


@lru_cache
def get_service() -> RagChatService:
    """Return a cached :class:`RagChatService` singleton."""
    return RagChatService(get_settings())


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional settings override.

    Returns:
        A configured :class:`fastapi.FastAPI` instance.
    """
    settings = settings or get_settings()
    configure_logging(settings)

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Enterprise RAG chat/query API built on LangChain.",
    )

    @app.get("/health", response_model=HealthStatus, tags=["ops"])
    def health() -> HealthStatus:
        """Liveness probe."""
        return HealthStatus(status="ok", service=settings.app_name, version=__version__)

    @app.get("/ready", response_model=HealthStatus, tags=["ops"])
    def ready() -> HealthStatus:
        """Readiness probe."""
        return HealthStatus(status="ok", service=settings.app_name, version=__version__)

    @app.post("/chat", response_model=ChatResponse, tags=["rag"])
    def chat(
        request: ChatRequest,
        service: RagChatService = Depends(get_service),
    ) -> ChatResponse:
        """Answer a message within a conversation session."""
        return service.chat(request.session_id, request.message)

    @app.post("/query", response_model=QueryResponse, tags=["rag"])
    def query(
        request: QueryRequest,
        service: RagChatService = Depends(get_service),
    ) -> QueryResponse:
        """Answer a stateless question."""
        return service.query(request.question, request.top_k)

    @app.post("/ingest", response_model=IngestResponse, tags=["rag"])
    def ingest(
        request: IngestRequest,
        service: RagChatService = Depends(get_service),
    ) -> IngestResponse:
        """Embed and index documents into the vector store."""
        return service.ingest(request.documents, request.metadata)

    logger.info("Created app %s v%s", settings.app_name, __version__)
    return app


app = create_app()


def main() -> None:
    """Run the development server."""
    import uvicorn

    uvicorn.run("langchain_rag.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
