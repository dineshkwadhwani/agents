"""
OrchestratorAgent

Responsibility: coordinate Planner, Researcher, Writer and Critic; decide
what happens next based on what the Critic actually found, rather than
running a fixed number of steps regardless of outcome.

This is the piece that distinguishes this system from a workflow: if the
Critic approves, the run ends immediately. If the Critic rejects, the
Orchestrator inspects *why*, sends the Researcher back to investigate that
specific gap, has the Writer revise (not regenerate) the draft, and re-submits
to the Critic -- up to max_iterations. A workflow would not branch on the
Critic's verdict at all.
"""
from __future__ import annotations

from agents.memory import SharedMemory
from agents import critic, planner, researcher, writer

NAME = "OrchestratorAgent"


def run(topic: str, target_length_words: int = 500, max_iterations: int = 3) -> dict:
    memory = SharedMemory()

    memory.log(sender=NAME, recipient="PlannerAgent", content=f"New run: topic='{topic}'")
    sub_questions = planner.plan(memory, topic, target_length_words)

    researcher.research(memory, sub_questions)
    current_draft = writer.draft(memory, topic)

    verdict = critic.review(memory, current_draft)
    iterations_used = 1

    while not verdict["approved"] and iterations_used < max_iterations:
        gap = verdict["gap"]
        memory.log(
            sender=NAME,
            recipient="ResearcherAgent",
            content=f"Critic rejected draft (score={verdict['score']}). Re-investigating gap: '{gap}'.",
        )
        new_finding = researcher.refine(memory, gap)
        current_draft = writer.revise(memory, gap, new_finding)
        verdict = critic.review(memory, current_draft)
        iterations_used += 1

    status = "approved" if verdict["approved"] else "max_iterations_reached"
    memory.log(
        sender=NAME,
        recipient="System",
        content=f"Run finished: status={status}, iterations_used={iterations_used}",
    )

    return {
        "report": current_draft,
        "iterations_used": iterations_used,
        "critic_final_score": verdict["score"],
        "status": status,
        "agent_trace": memory.as_trace(),
    }
