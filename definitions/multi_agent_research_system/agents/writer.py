"""
WriterAgent

Responsibility: turn the Planner's structure plus the Researcher's findings
into a coherent draft report. On a second pass (after a Critic rejection),
this agent incorporates the newly-refined finding into the existing draft
rather than starting over -- it revises, it doesn't just regenerate blindly.
"""
from __future__ import annotations

from agents.memory import SharedMemory

NAME = "WriterAgent"


def draft(memory: SharedMemory, topic: str) -> str:
    sections = [f"# Report: {topic}\n"]
    for question, answer in memory.findings.items():
        sections.append(f"## {question}\n{answer}\n")
    report = "\n".join(sections)
    memory.drafts.append(report)
    memory.log(sender=NAME, recipient="CriticAgent", content="Draft ready for review.")
    return report


def revise(memory: SharedMemory, gap: str, new_finding: str) -> str:
    """Incorporate one specific new finding into the most recent draft."""
    previous = memory.drafts[-1]
    addition = f"\n## Follow-up: {gap}\n{new_finding}\n"
    revised = previous + addition
    memory.drafts.append(revised)
    memory.log(
        sender=NAME,
        recipient="CriticAgent",
        content=f"Draft revised to address flagged gap: '{gap}'.",
    )
    return revised
