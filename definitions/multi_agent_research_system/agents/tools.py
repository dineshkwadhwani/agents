"""
Tools available to agents. Kept intentionally small and dependency-free so this
sample project runs offline, with no API keys required -- the point of this repo
is to demonstrate a genuine multi-agent *architecture*, not to be a production
research product.

mock_search is a stand-in for a real web-search tool (e.g. Tavily, Serper,
Bing). Swapping it for a real API call does not change any agent or
orchestrator logic below -- agents call tools by name and reason about the
result, they don't know or care how the tool is implemented.
"""
from __future__ import annotations

import re

# A tiny canned knowledge base, keyed by fuzzy topic match, so the demo
# produces plausible, varied findings without calling out to the network.
_KNOWLEDGE_BASE = {
    "multi-agent systems": (
        "Multi-agent systems decompose a task across several autonomous agents that "
        "each reason independently and coordinate through messages or shared state, "
        "in contrast to a single monolithic agent or a fixed pipeline."
    ),
    "orchestration patterns": (
        "Common orchestration patterns include orchestrator-worker (a central agent "
        "delegates and arbitrates), peer-to-peer (agents negotiate directly), and "
        "blackboard (agents read/write a shared workspace, as in this project)."
    ),
    "agent vs workflow": (
        "The key distinction is adaptivity: a workflow executes a fixed sequence "
        "regardless of intermediate results, while an agentic system re-plans its "
        "next action based on what was just discovered, including retrying or "
        "escalating on failure."
    ),
    "evaluation of agentic systems": (
        "Agentic systems are commonly evaluated on task success rate, number of "
        "steps/iterations to success, groundedness of outputs, and robustness to "
        "tool failures -- not just final-answer accuracy."
    ),
}


def mock_search(query: str) -> str:
    """Return a canned but topic-relevant search result for a sub-question."""
    query_lower = query.lower()
    for key, answer in _KNOWLEDGE_BASE.items():
        if key in query_lower:
            return answer
    # Fallback so the demo never returns an empty result for an unseen sub-question.
    return (
        f"No indexed source matched '{query}' directly; recommend the Researcher "
        f"agent flag this sub-question as needing a follow-up search with refined "
        f"terms."
    )


_ALLOWED_CHARS = re.compile(r"^\s*[\d\s+\-*/().]+\s*$")


def calculator(expression: str) -> str:
    """A small, safe arithmetic tool -- demonstrates a second, distinct tool type."""
    if not _ALLOWED_CHARS.match(expression):
        return "error: expression contains unsupported characters"
    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return str(result)
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"
