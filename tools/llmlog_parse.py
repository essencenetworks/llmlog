#!/usr/bin/env python3
"""
llmlog_parse.py — example parser for LLMLOG/1.0 blocks.
- Reads a text file (or stdin) containing one or more blocks
- Emits JSON Lines: one object per block
- Zero dependencies; Python 3.10+

Usage:
  python llmlog_parse.py file.txt > out.jsonl
  cat file.txt | python llmlog_parse.py
"""
from __future__ import annotations
import re, sys, json
from pathlib import Path
from typing import Dict, List

BEGIN_RE = re.compile(r"^LLMLOG/(?P<ver>\d+\.\d+) BEGIN (?P<kv>.+)$", re.M)
END_RE   = re.compile(r"^LLMLOG/(?P<ver>\d+\.\d+) END\s*$", re.M)

def _normalise_tags(s: str) -> List[str]:
    tags = [t.strip().lower() for t in s.split(',') if t.strip()]
    seen, out = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t); out.append(t)
    return out

def parse_kv(s: str) -> Dict[str, object]:
    # Parse space-separated key=value pairs. Values cannot contain spaces.
    # Unknown keys preserved (as strings).
    out: Dict[str, object] = {}
    for token in s.strip().split():
        if "=" in token:
            k, v = token.split("=", 1)
            out[k.strip()] = v.strip()
    # spelling & legacy normalisation
    if "organisation" not in out:
        if "organization" in out: out["organisation"] = out.pop("organization")
        if "starship" in out and "organisation" not in out:
            out["organisation"] = out.pop("starship")
    # tags normalisation
    tags_str = out.get("tags") or out.get("tag")
    if isinstance(tags_str, str) and tags_str:
        out["tags"] = _normalise_tags(tags_str)
        out.pop("tag", None)
    return out

def extract_blocks(text: str):
    begins = list(BEGIN_RE.finditer(text))
    ends   = list(END_RE.finditer(text))
    for i, b in enumerate(begins):
        start_body = b.end()
        e = next((e for e in ends if e.start() > start_body), None)
        if not e:
            continue
        body = text[start_body:e.start()]
        def grab(label: str) -> str:
            m = re.search(rf"^{label}:\s*\n(?P<val>(?:.+\n)*?)(?=^\w+:|\Z)", body, re.M)
            if not m: return ""
            raw = m.group("val").strip("\n")
            lines = [ln.strip().strip('“”"') for ln in raw.splitlines()]
            return "\n".join(lines).strip()
        meta = parse_kv(b.group("kv"))
        yield {
            "version": b.group("ver"),
            **meta,
            "entry":   grab("entry"),
            "mission": grab("mission"),
            "outcome": grab("outcome"),
        }

def main():
    if len(sys.argv) > 1:
        data = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        data = sys.stdin.read()
    for rec in extract_blocks(data):
        sys.stdout.write(json.dumps(rec, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
