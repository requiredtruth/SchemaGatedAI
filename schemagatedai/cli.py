from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
from .gate import GateError, SchemaGate

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reject impossible streamed JSON before storing it.")
    parser.add_argument("schema")
    parser.add_argument("--chunk", type=int, default=64)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args(argv)
    try:
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
        gate = SchemaGate(schema, max_bytes=args.max_bytes)
        while data := sys.stdin.read(args.chunk):
            gate.feed(data)
        value = gate.finish()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"schemagatedai: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(value, sort_keys=True))
    return 0
