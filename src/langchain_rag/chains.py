"""LangChain RAG chain assembly.

Builds retrieval-augmented generation chains from a retriever, an LLM, and a
prompt template. Functions construct and return chain objects but never invoke
them at import time, so importing this module has no external side effects.
"""

from __future__ import annotations

from typing import Any

from langchain_rag.config import Settings, get_settings
from langchain_rag.logging_config import get_logger
from langchain_rag.retrievers import build_retriever

logger = get_logger(__name__)

_SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. Answer the question using only "
    "the provided context. If the context is insufficient, say so plainly.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
)


def build_llm(settings: Settings | None = None) -> Any:
    """Build the chat LLM used to synthesise answers.

    Args:
        settings: Optional settings override.

    Returns:
        A LangChain chat model instance.
    """
    settings = settings or get_settings()
    from langchain_openai import ChatOpenAI

    logger.debug("Building LLM %s (temp=%s)", settings.llm_model, settings.temperature)
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.temperature,
        api_key=settings.openai_api_key,
    )


def build_prompt() -> Any:
    """Build the RAG prompt template."""
    from langchain_core.prompts import ChatPromptTemplate

    return ChatPromptTemplate.from_template(_SYSTEM_PROMPT)


def build_rag_chain(
    settings: Settings | None = None,
    retriever: Any | None = None,
    llm: Any | None = None,
) -> Any:
    """Assemble a retrieval-QA chain.

    The chain retrieves relevant documents, formats them into the prompt
    context, invokes the LLM, and parses the string output.

    Args:
        settings: Optional settings override.
        retriever: Optional pre-built retriever.
        llm: Optional pre-built chat model.

    Returns:
        A runnable LangChain chain.
    """
    settings = settings or get_settings()
    retriever = retriever or build_retriever(settings)
    llm = llm or build_llm(settings)
    prompt = build_prompt()

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    def _format_docs(docs: list[Any]) -> str:
        return "\n\n".join(getattr(d, "page_content", str(d)) for d in docs)

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.debug("Assembled RAG chain")
    return chain
