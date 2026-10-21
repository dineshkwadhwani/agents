# Input / Output Specification

## Input

Invoked via CLI (`main.py`), HTTP (`POST /run` via `api.py`), or directly via
`agents.orchestrator.run(...)`.

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | string | yes | The research topic. |
| `target_length_words` | int | no (default 500) | Desired report length; controls Planner's plan depth. |
| `max_iterations` | int | no (default 3) | Max Researcher/Writer/Critic replanning loops before giving up. |

### Sample input (CLI)
```bash
python main.py --topic "multi-agent systems" --length 700 --save-trace execution_traces/run.json
```

### Sample input (HTTP)
```bash
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" \
  -d '{"topic": "multi-agent systems", "target_length_words": 700}'
```

## Output

A single dict (JSON-serializable):

```json
{
  "report": "string, the final markdown report",
  "iterations_used": 1,
  "critic_final_score": 0.9,
  "status": "approved",
  "agent_trace": [
    {
      "sender": "PlannerAgent",
      "recipient": "ResearcherAgent",
      "content": "Plan created for topic '...': [...]",
      "timestamp": 1730000000.123
    }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `report` | string | The final markdown-formatted report. |
| `iterations_used` | int | How many Researcher/Writer/Critic cycles actually ran. |
| `critic_final_score` | float (0-1) | The Critic's score on the final accepted (or last attempted) draft. |
| `status` | `"approved"` \| `"max_iterations_reached"` | Whether the Critic approved the draft or the loop was exhausted. |
| `agent_trace` | list of message objects | The full inter-agent message log — this is the artifact submitted as the "Agent Execution Trace" for CA3. |
