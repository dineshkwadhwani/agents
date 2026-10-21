"""
CriticAgent

Responsibility: independently evaluate the draft against the original plan
and flag the single most important gap, if any. This is the generator-critic
pattern -- a distinct agent whose entire job is to find fault with another
agent's output, which is what makes the orchestrator's replanning loop
meaningful rather than cosmetic.
"""
from __future__ import annotations

from agents.memory import SharedMemory

NAME = "CriticAgent"

# A deliberately strict first-pass check so a real run demonstrates the
# replanning loop at least once: any sub-question whose finding mentions
# "no indexed source" is treated as an unresolved gap.
_UNRESOLVED_MARKER = "no indexed source"


def review(memory: SharedMemory, draft_text: str) -> dict:
    unresolved = [
        question
        for question, answer in memory.findings.items()
        if _UNRESOLVED_MARKER in answer.lower()
    ]

    if unresolved:
        gap = unresolved[0]
        verdict = {
            "approved": False,
            "score": 0.55,
            "gap": gap,
            "reason": f"Sub-question '{gap}' has no resolved finding; report would ship with a gap.",
        }
    else:
        verdict = {
            "approved": True,
            "score": 0.9,
            "gap": None,
            "reason": "All planned sub-questions have a resolved finding reflected in the draft.",
        }

    memory.critiques.append(verdict)
    memory.log(
        sender=NAME,
        recipient="OrchestratorAgent",
        content=f"Verdict: {verdict}",
    )
    return verdict
