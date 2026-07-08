"""Tests for windowed conversation memory."""

from __future__ import annotations

from langchain_rag.memory import WindowedConversationMemory


def test_memory_keeps_last_n_turns() -> None:
    memory = WindowedConversationMemory(window=3)
    for i in range(5):
        memory.add_turn(f"question {i}", f"answer {i}")

    turns = memory.turns
    assert len(turns) == 3
    # Oldest retained turn should be turn index 2 (0 and 1 evicted).
    assert turns[0][0].content == "question 2"
    assert turns[-1][1].content == "answer 4"


def test_memory_messages_are_flattened_in_order() -> None:
    memory = WindowedConversationMemory(window=2)
    memory.add_turn("hi", "hello")
    memory.add_turn("bye", "goodbye")

    messages = memory.messages()
    assert [m.role for m in messages] == ["user", "assistant", "user", "assistant"]
    assert [m.content for m in messages] == ["hi", "hello", "bye", "goodbye"]


def test_memory_clear() -> None:
    memory = WindowedConversationMemory(window=2)
    memory.add_turn("a", "b")
    memory.clear()
    assert memory.turns == []
