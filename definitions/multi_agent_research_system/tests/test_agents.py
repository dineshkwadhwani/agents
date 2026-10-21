from agents.memory import SharedMemory
from agents import critic, planner, researcher, writer
from agents.orchestrator import run
from agents.tools import calculator, mock_search


def test_planner_depth_scales_with_target_length():
    memory = SharedMemory()
    short_plan = planner.plan(memory, "multi-agent systems", target_length_words=200)
    memory2 = SharedMemory()
    long_plan = planner.plan(memory2, "multi-agent systems", target_length_words=1000)
    assert len(short_plan) < len(long_plan)


def test_researcher_routes_arithmetic_to_calculator():
    memory = SharedMemory()
    findings = researcher.research(memory, ["2 + 2"])
    assert findings["2 + 2"] == "4"


def test_researcher_routes_topic_question_to_search():
    memory = SharedMemory()
    findings = researcher.research(memory, ["What are orchestration patterns?"])
    assert "orchestrator-worker" in findings["What are orchestration patterns?"].lower()


def test_researcher_does_not_misroute_hyphenated_prose_to_calculator():
    memory = SharedMemory()
    findings = researcher.research(memory, ["How does multi-agent systems differ from related but simpler approaches?"])
    result = findings["How does multi-agent systems differ from related but simpler approaches?"]
    assert not result.startswith("error")


def test_critic_flags_unresolved_gap():
    memory = SharedMemory()
    memory.findings = {"unknown topic xyz": "No indexed source matched 'unknown topic xyz' directly"}
    draft_text = writer.draft(memory, "unknown topic xyz")
    verdict = critic.review(memory, draft_text)
    assert verdict["approved"] is False
    assert verdict["gap"] == "unknown topic xyz"


def test_critic_approves_when_all_findings_resolved():
    memory = SharedMemory()
    memory.findings = {"What is multi-agent systems?": mock_search("multi-agent systems")}
    draft_text = writer.draft(memory, "multi-agent systems")
    verdict = critic.review(memory, draft_text)
    assert verdict["approved"] is True


def test_orchestrator_replans_on_rejection_and_eventually_terminates():
    result = run(topic="a totally unindexed niche topic", target_length_words=300, max_iterations=3)
    assert result["status"] in ("approved", "max_iterations_reached")
    assert result["iterations_used"] >= 1
    assert len(result["agent_trace"]) > 0
    senders = {m["sender"] for m in result["agent_trace"]}
    assert {"PlannerAgent", "ResearcherAgent", "WriterAgent", "CriticAgent", "OrchestratorAgent"} <= senders


def test_calculator_rejects_unsafe_input():
    assert calculator("__import__('os')").startswith("error")


def test_calculator_evaluates_safe_expression():
    assert calculator("(2 + 3) * 4") == "20"
