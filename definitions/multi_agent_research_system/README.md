# Multi-Agent Research & Report System

A small, offline-runnable demonstration of a genuinely agentic multi-agent
system: four specialized agents (Planner, Researcher, Writer, Critic)
coordinated by an Orchestrator that **replans based on the Critic's actual
verdict**, rather than running a fixed sequence of steps.

See [`docs/DESIGN.md`](docs/DESIGN.md) for the full architecture and
[`docs/INPUT_OUTPUT_SPEC.md`](docs/INPUT_OUTPUT_SPEC.md) for the input/output
contract.

## Quick start

```bash
pip install -r requirements.txt
python main.py --topic "multi-agent systems" --length 700 --save-trace execution_traces/run.json
```

## Quick start (HTTP API)

```bash
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
```
```bash
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" \
  -d '{"topic": "multi-agent systems", "target_length_words": 700}'
```

## Run tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Project structure

```
agents/
  memory.py        shared blackboard all agents read/write
  tools.py         mock_search + calculator tools
  planner.py       PlannerAgent
  researcher.py    ResearcherAgent
  writer.py        WriterAgent
  critic.py        CriticAgent
  orchestrator.py  coordinates the above; owns the replanning loop
docs/
  DESIGN.md              architecture, orchestration pattern, diagram
  INPUT_OUTPUT_SPEC.md    input/output schema + samples
execution_traces/
  sample_run.json           a run that triggers the Critic-rejection replanning loop
  sample_run_approved.json  a run approved on the first pass, for contrast
tests/
  test_agents.py    unit tests per agent + an end-to-end orchestrator test
main.py             CLI entrypoint
api.py              HTTP wrapper (no agent logic) for hosted deployment
Dockerfile          builds the api.py service for Render (or any Docker host)
```

## Why this counts as agents, not a workflow

Every step here could be wired as a fixed n8n/Zapier chain instead: Plan →
Research → Write → Critique, always in that order, always the same number
of steps. What makes this a multi-agent *system* rather than that chain is
in `agents/orchestrator.py`: the next action depends on what the Critic
actually found. Approval ends the run immediately. Rejection sends the
Researcher back to investigate the *specific* gap the Critic named, has the
Writer revise the existing draft, and resubmits — up to a bounded number of
attempts, after which the system reports honest partial failure rather than
looping forever or silently shipping an incomplete report.
