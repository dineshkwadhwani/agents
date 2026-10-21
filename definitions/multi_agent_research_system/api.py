"""
Thin HTTP wrapper around the multi-agent core, for hosted deployment.

IMPORTANT: this file contains no agent logic. Its only job is: accept a
request, call agents.orchestrator.run(...), persist the full trace to disk,
and return the result. Every planning, research, drafting and critique
decision still happens inside agents/*.py, exactly as the CLI runs it.
"""
from __future__ import annotations

import json
import os
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from agents.orchestrator import run

app = FastAPI(title="Multi-Agent Research System API")

TRACE_DIR = os.environ.get("TRACE_DIR", "execution_traces")
os.makedirs(TRACE_DIR, exist_ok=True)


class RunRequest(BaseModel):
    topic: str
    target_length_words: int = 500
    max_iterations: int = 3


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
def run_agents(req: RunRequest):
    result = run(
        topic=req.topic,
        target_length_words=req.target_length_words,
        max_iterations=req.max_iterations,
    )

    trace_id = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    trace_path = os.path.join(TRACE_DIR, f"run_{trace_id}.json")
    with open(trace_path, "w") as f:
        json.dump(result, f, indent=2)

    return {**result, "trace_file": trace_path}
