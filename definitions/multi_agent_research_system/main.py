#!/usr/bin/env python3
"""
CLI entrypoint. Example:

    python main.py --topic "multi-agent systems" --length 600
"""
from __future__ import annotations

import argparse
import json
import sys

from agents.orchestrator import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the multi-agent research system.")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--length", type=int, default=500, help="Target report length in words")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max Researcher/Writer/Critic loops")
    parser.add_argument("--save-trace", help="Optional path to write the full execution trace as JSON")
    args = parser.parse_args()

    result = run(topic=args.topic, target_length_words=args.length, max_iterations=args.max_iterations)

    print(result["report"])
    print("\n---")
    print(f"status: {result['status']}")
    print(f"iterations_used: {result['iterations_used']}")
    print(f"critic_final_score: {result['critic_final_score']}")

    if args.save_trace:
        with open(args.save_trace, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nFull execution trace written to {args.save_trace}")


if __name__ == "__main__":
    sys.exit(main())
