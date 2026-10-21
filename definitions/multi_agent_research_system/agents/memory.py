"""
Shared working memory ("blackboard") for a single research run.

Every agent reads from and writes to the same SharedMemory instance for the
duration of one run. This is what lets the Critic's feedback actually change
what the Researcher or Writer do next -- agents are coordinating through
shared state and messages, not just handing a fixed payload down a pipeline.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    sender: str
    recipient: str
    content: str
    timestamp: float = field(default_factory=time.time)


class SharedMemory:
    def __init__(self) -> None:
        self.plan: list[str] = []
        self.findings: dict[str, str] = {}          # sub_question -> researched answer
        self.drafts: list[str] = []                  # every draft version, latest last
        self.critiques: list[dict[str, Any]] = []    # every critique issued, in order
        self.messages: list[Message] = []            # full inter-agent message log

    def log(self, sender: str, recipient: str, content: str) -> None:
        self.messages.append(Message(sender=sender, recipient=recipient, content=content))

    def as_trace(self) -> list[dict[str, Any]]:
        """Serialize the full run as an execution trace (agent <-> agent messages)."""
        return [
            {
                "sender": m.sender,
                "recipient": m.recipient,
                "content": m.content,
                "timestamp": m.timestamp,
            }
            for m in self.messages
        ]
