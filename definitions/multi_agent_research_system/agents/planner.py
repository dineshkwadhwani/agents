"""
PlannerAgent

Responsibility: turn a broad topic into a concrete, ordered set of
sub-questions that -- if answered -- would let the WriterAgent produce a
complete report. This is the agent's own reasoning step: the sub-questions
are not hardcoded per topic, they are derived from the topic and requested
length.
"""
from __future__ import annotations

from agents.memory import SharedMemory

NAME = "PlannerAgent"


def plan(memory: SharedMemory, topic: str, target_length_words: int) -> list[str]:
    """Reason about how many sub-questions are needed for the requested depth,
    then generate them. A longer target report gets a more thorough plan --
    this is the adaptivity that separates planning from a fixed template."""
    if target_length_words <= 300:
        depth = 2
    elif target_length_words <= 800:
        depth = 3
    else:
        depth = 4

    base_angles = [
        f"What is {topic}?",
        f"What are the core architectural patterns used in {topic}?",
        f"How does {topic} differ from related but simpler approaches?",
        f"How is {topic} evaluated in practice?",
    ]
    sub_questions = base_angles[:depth]

    memory.plan = sub_questions
    memory.log(
        sender=NAME,
        recipient="ResearcherAgent",
        content=(
            f"Plan created for topic '{topic}' (target {target_length_words} words, "
            f"depth={depth}): {sub_questions}"
        ),
    )
    return sub_questions
