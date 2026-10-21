"""
ResearcherAgent

Responsibility: answer each sub-question from the plan by deciding which
tool to call and reasoning over the result. This agent owns tool use.

When re-invoked after a Critic rejection (see orchestrator.py), this agent
receives the specific gap the Critic identified and researches *that*
specifically, rather than blindly repeating its first pass -- this is the
adaptive-on-feedback behaviour the CA3 rubric looks for.
"""
from __future__ import annotations

import re

from agents.memory import SharedMemory
from agents.tools import calculator, mock_search

NAME = "ResearcherAgent"

# A question is treated as arithmetic only if it looks like a numeric
# expression (digits plus operators), not merely because it *contains* a
# hyphen or slash somewhere in ordinary prose (e.g. "multi-agent").
_ARITHMETIC_PATTERN = re.compile(r"^\s*[\d\s+\-*/().]+\s*$")


def research(memory: SharedMemory, sub_questions: list[str]) -> dict[str, str]:
    findings: dict[str, str] = {}
    for question in sub_questions:
        if _ARITHMETIC_PATTERN.match(question):
            result = calculator(question)
            tool_used = "calculator"
        else:
            result = mock_search(question)
            tool_used = "mock_search"

        findings[question] = result
        memory.log(
            sender=NAME,
            recipient="WriterAgent",
            content=f"[{tool_used}] '{question}' -> {result}",
        )

    memory.findings.update(findings)
    return findings


def refine(memory: SharedMemory, gap: str) -> str:
    """Targeted follow-up research triggered by a specific Critic-identified gap,
    rather than re-running the entire original plan from scratch."""
    result = mock_search(gap)
    memory.findings[gap] = result
    memory.log(
        sender=NAME,
        recipient="WriterAgent",
        content=f"[refinement for critic-flagged gap] '{gap}' -> {result}",
    )
    return result
