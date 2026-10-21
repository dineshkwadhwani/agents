# Design Document — Multi-Agent Research & Report System

## 1. Problem & Approach

Producing a well-scoped research report requires: deciding what sub-questions
matter, gathering evidence for each, drafting a coherent write-up, and
critically checking the result before it ships. A single LLM call conflates
all four steps into one undifferentiated pass with no internal check. This
system separates them into four agents with distinct responsibilities and a
fifth coordinating role, so that quality control is a real, separate step —
not something hoped for inside one big prompt.

## 2. Agents

| Agent | Responsibility | Tools Used |
|---|---|---|
| **PlannerAgent** | Decomposes the topic into an ordered list of sub-questions, scaling plan depth to the requested report length. | none |
| **ResearcherAgent** | Answers each sub-question by choosing and calling the appropriate tool; on re-invocation, targets only the specific gap the Critic flagged. | `mock_search`, `calculator` |
| **WriterAgent** | Drafts the report from the Planner's structure and the Researcher's findings; on revision, incorporates new findings into the existing draft rather than regenerating from scratch. | none |
| **CriticAgent** | Independently reviews the draft against the original plan and flags the single most important unresolved gap, if any. | none |
| **OrchestratorAgent** | Coordinates the other four; decides whether to terminate or replan based on the Critic's actual verdict. | none (coordination only) |

## 3. Orchestration Pattern: Orchestrator-Worker with a Critic Loop

```
   ┌─────────────┐
   │   Planner   │  topic -> sub-questions
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ Researcher  │◄──────────────┐
   └──────┬──────┘                │ gap (if rejected)
          ▼                       │
   ┌─────────────┐                │
   │   Writer    │◄───────────┐   │
   └──────┬──────┘            │   │
          ▼                   │   │
   ┌─────────────┐   reject   │   │
   │   Critic    ├────────────┴───┘
   └──────┬──────┘
          │ approve
          ▼
   ┌─────────────┐
   │   Report    │
   └─────────────┘
```

This is an **orchestrator-worker with a generator-critic loop**: the
Orchestrator does not simply run each agent once in sequence. It inspects
the Critic's verdict and, on rejection, sends the Researcher back to
investigate the *specific* flagged gap (not the whole plan again), then has
the Writer revise (not regenerate) the draft, then re-submits to the Critic.
This repeats up to `max_iterations`. If the gap still cannot be resolved,
the run terminates honestly with `status: max_iterations_reached` rather
than silently shipping a report with a known hole in it.

This loop is what a fixed workflow cannot do: a workflow would run
Plan → Research → Write → (maybe) Critique once, in that order, regardless
of what the Critic found, because there is no branch in a fixed pipeline
that depends on the Critic's *content*, only (at best) on whether it errored.

## 4. Shared Memory

All agents read from and write to one `SharedMemory` instance per run
(`agents/memory.py`). It holds:
- `plan`: the Planner's sub-questions
- `findings`: sub-question → researched answer
- `drafts`: every draft version produced, latest last
- `critiques`: every Critic verdict issued, in order
- `messages`: the full inter-agent message log (this is what becomes the
  Execution Trace artifact)

This is a blackboard pattern: agents coordinate through shared state rather
than only through direct function-call return values, which is what makes
the full message history available as a genuine trace of *inter-agent*
communication, not just a call stack.

## 5. Tools

- `mock_search(query)`: stands in for a real web-search API (Tavily, Serper,
  Bing, etc.). Swapping in a real API changes nothing about any agent's
  logic — agents call a tool by name and reason about its text result.
- `calculator(expression)`: a small, safe arithmetic evaluator, included to
  demonstrate that the Researcher genuinely chooses between more than one
  tool type based on the sub-question, rather than always calling the same
  one.

## 6. Failure Handling

If the Critic's flagged gap cannot be resolved within `max_iterations`, the
system does not loop forever and does not silently present an incomplete
report as final. It returns `status: max_iterations_reached` alongside the
best draft achieved, so a caller (or a human) can decide what to do next.
This is a deliberate design choice: graceful, honest degradation rather than
either infinite retries or a confidently wrong final answer.

## 7. Tech Stack

- Python 3.12, standard library only for the agent core (no external
  services required to run the demo — see Section 5 on tools for why
  that's safe to say).
- `pytest` for tests.
- `FastAPI` + `uvicorn` for the HTTP wrapper (`api.py`) used in deployment.
- No database: state lives only in the per-run `SharedMemory` instance.

## 8. Deployment Architecture

Deployed as a single Docker container (see `Dockerfile`) running the FastAPI
wrapper in `api.py`. The wrapper contains **no agent logic** — it accepts a
request, calls `agents.orchestrator.run(...)`, persists the resulting trace,
and returns it. Every planning, research, drafting and critique decision
still happens inside `agents/*.py`, identically to running the CLI locally.
