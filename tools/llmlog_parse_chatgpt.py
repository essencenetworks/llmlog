#!/usr/bin/env python3
"""
Extract LLMLOG/1.0 blocks from a ChatGPT data export ZIP or folder and write CSV/NDJSON.

Usage:
  python llmlog_parse.py /path/to/chatgpt-export.zip --out-csv llmlog_export.csv
  python llmlog_parse.py /path/to/export-folder --out-csv llmlog_export.csv --out-ndjson llmlog_export.ndjson

Notes:
  - Use this on your ChatGPT data export ZIP (Settings → Data Controls → Export data); the download contains conversations.json that this script parses.
  - Looks for 'conversations.json' inside the export.
  - Works even if code fences are present; parses by BEGIN/END.
  - Unifies 'organisation'/'organization' to 'org' in output; original key is preserved.

Maintained by Essence Networks Limited. MIT Licence.
"""
import argparse, csv, io, json, os, re, sys, tempfile, zipfile
from pathlib import Path

BEGIN_RE = re.compile(r"LLMLOG/1\.0\s+BEGIN\s+(?P<kvs>[^\n\r]+)")
END_RE = re.compile(r"^\s*LLMLOG/1\.0\s+END\s*$", re.M)
BLOCK_RE = re.compile(r"(?:```.*?\n)?\s*LLMLOG/1\.0\s+BEGIN.*?LLMLOG/1\.0\s+END\s*(?:\n```)?", re.S)
KV_RE = re.compile(r"([A-Za-z][A-Za-z_-]*)=([^\s]+)")
LABEL_RE = re.compile(r"^(entry|mission|outcome):\s*$")

def find_conversations_json(root: Path) -> Path:
    candidates = list(root.rglob("conversations.json"))
    if not candidates:
        raise FileNotFoundError("Could not find conversations.json under: %s" % root)
    # prefer shortest path
    return sorted(candidates, key=lambda p: len(str(p)))[0]

def load_export(path: Path) -> Path:
    if path.is_dir():
        return path
    if path.suffix.lower() == ".zip":
        tmpdir = Path(tempfile.mkdtemp(prefix="chatgpt_export_"))
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(tmpdir)
        return tmpdir
    raise ValueError("Path must be a folder or a .zip file")

def iter_conversations(conv_json) -> tuple:
    # Support both list of conversations or dict with 'conversations'
    if isinstance(conv_json, dict) and "conversations" in conv_json:
        convs = conv_json["conversations"]
    else:
        convs = conv_json
    if not isinstance(convs, list):
        raise ValueError("Unexpected conversations.json structure")
    for conv in convs:
        # Best-effort ids/titles across formats
        cid = conv.get("conversation_id") or conv.get("id") or conv.get("conversationId") or ""
        title = conv.get("title") or ""
        yield cid, title, conv

def extract_blocks_from_text(text: str):
    for m in BLOCK_RE.finditer(text):
        yield m.group(0)

def parse_begin_kvs(begin_line: str) -> dict:
    kvs = {}
    for k, v in KV_RE.findall(begin_line):
        kvs[k] = v
    # normalize tags
    if "tags" in kvs:
        tags = [t.strip().lower() for t in kvs["tags"].split(",") if t.strip()]
        seen = set(); norm = []
        for t in tags:
            if t not in seen:
                norm.append(t); seen.add(t)
        kvs["tags"] = norm
    return kvs

def parse_body(block_text: str) -> dict:
    """
    Parse the body sections entry/mission/outcome (each as free text until the next label or END).
    """
    # Strip surrounding fences if any
    if block_text.strip().startswith("```"):
        # remove first fence line and trailing fence if present
        lines = block_text.strip().splitlines()
        # drop first
        lines = lines[1:]
        # drop trailing fence if last line is ```
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    else:
        text = block_text

    # Grab BEGIN line
    mb = BEGIN_RE.search(text)
    if not mb:
        raise ValueError("BEGIN line not found")
    begin_line = mb.group(0)
    kvs = parse_begin_kvs(mb.group("kvs"))

    # Body after BEGIN line
    after = text[mb.end():]
    # We'll parse labels by scanning lines
    current = None
    sections = {"entry": [], "mission": [], "outcome": []}
    for raw in after.splitlines():
        if END_RE.search(raw):
            break
        m = LABEL_RE.match(raw.strip())
        if m:
            current = m.group(1)
            continue
        if current:
            # strip exactly two leading spaces if present
            line = raw[2:] if raw.startswith("  ") else raw
            sections[current].append(line.rstrip())

    # Join and trim extra empty lines
    body = {k: "\n".join([ln for ln in v]).strip() for k, v in sections.items()}
    return begin_line, kvs, body

def records_from_conversation(cid: str, title: str, conv_obj) -> list:
    text = json.dumps(conv_obj, ensure_ascii=False)
    recs = []
    for block in extract_blocks_from_text(text):
        try:
            begin_line, kvs, body = parse_body(block)
        except Exception:
            continue
        # org normalization
        org_key = "organisation" if "organisation" in kvs else ("organization" if "organization" in kvs else None)
        org = kvs.get(org_key) if org_key else ""
        rec = {
            "conversation_id": cid,
            "conversation_title": title,
            "project": kvs.get("project",""),
            "org": org,
            "org_key": org_key or "",
            "date": kvs.get("date",""),
            "tags": ",".join(kvs.get("tags", [])),
            "entry": body.get("entry",""),
            "mission": body.get("mission",""),
            "outcome": body.get("outcome",""),
            "begin_line": begin_line.strip(),
        }
        recs.append(rec)
    return recs

def main():
    ap = argparse.ArgumentParser(description="Extract LLMLOG/1.0 blocks from ChatGPT data export")
    ap.add_argument("path", help="Path to ChatGPT export ZIP or folder")
    ap.add_argument("--out-csv", default="llmlog_export.csv", help="Output CSV path")
    ap.add_argument("--out-ndjson", default=None, help="Optional NDJSON output path")
    args = ap.parse_args()

    root = load_export(Path(args.path))
    conv_path = find_conversations_json(root)
    with open(conv_path, "r", encoding="utf-8") as f:
        conv_json = json.load(f)

    all_recs = []
    for cid, title, conv in iter_conversations(conv_json):
        all_recs.extend(records_from_conversation(cid, title, conv))

    # Write CSV
    fields = ["conversation_id","conversation_title","project","org","org_key","date","tags","entry","mission","outcome","begin_line"]
    with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in all_recs:
            w.writerow(r)

    # Write NDJSON if requested
    if args.out_ndjson:
        with open(args.out_ndjson, "w", encoding="utf-8") as f:
            for r in all_recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(all_recs)} records to {args.out_csv}" + (f" and {args.out_ndjson}" if args.out_ndjson else ""))

if __name__ == "__main__":
    main()
