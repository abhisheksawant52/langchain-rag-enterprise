"""Conversation memory wrapper.

Provides a lightweight windowed conversation buffer that keeps only the most
recent ``window`` turns (a user + assistant exchange counts as one turn). The
implementation is pure Python so it can be unit-tested without external
dependencies, and can also expose an equivalent LangChain memory object.
"""

from __future__ import annotations

from collections import deque
from typing import Any

from langchain_rag.config import get_settings
from langchain_rag.models import Message


class WindowedConversationMemory:
    """Keep the last ``window`` turns of a conversation.

    A "turn" is a (user, assistant) pair. Adding a new turn beyond the window
    evicts the oldest turn.
    """

    def __init__(self, window: int | None = None) -> None:
        """Initialise the memory.

        Args:
            window: Maximum number of turns to retain. Defaults to the
                configured ``memory_window`` setting.
        """
        self.window = window if window is not None else get_settings().memory_window
        self._turns: deque[tuple[Message, Message]] = deque(maxlen=self.window)

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        """Record a completed user/assistant exchange."""
        self._turns.append(
            (
                Message(role="user", content=user_message),
                Message(role="assistant", content=assistant_message),
            )
        )

    @property
    def turns(self) -> list[tuple[Message, Message]]:
        """Return the retained turns, oldest first."""
        return list(self._turns)

    def messages(self) -> list[Message]:
        """Return retained messages flattened in chronological order."""
        flat: list[Message] = []
        for user_msg, assistant_msg in self._turns:
            flat.append(user_msg)
            flat.append(assistant_msg)
        return flat

    def history_text(self) -> str:
        """Render the retained history as plain text for prompt injection."""
        return "\n".join(f"{m.role}: {m.content}" for m in self.messages())

    def clear(self) -> None:
        """Forget all retained turns."""
        self._turns.clear()

    def as_langchain_memory(self) -> Any:
        """Build an equivalent LangChain windowed buffer memory object."""
        from langchain.memory import ConversationBufferWindowMemory

        return ConversationBufferWindowMemory(
            k=self.window,
            memory_key="chat_history",
            return_messages=True,
        )
