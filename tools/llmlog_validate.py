#!/usr/bin/env python3
"""
llmlog_validate.py — strict fence + BEGIN keys validator for LLMLOG/1.0.
Exit status: 0 on success, 1 on failure.

Usage:
  python llmlog_validate.py file.txt
"""
import re, sys
if len(sys.argv) != 2:
    print("usage: python llmlog_validate.py <file>", file=sys.stderr)
    raise SystemExit(2)
t = open(sys.argv[1], encoding="utf-8").read()
begins = re.findall(r'^LLMLOG/\d+\.\d+ BEGIN (.*)$', t, re.M)
ends   = re.findall(r'^LLMLOG/\d+\.\d+ END\s*$', t, re.M)
keys_ok = all(('project=' in x and 'date=' in x and ('organisation=' in x or 'organization=' in x)) for x in begins)
if begins and len(begins) == len(ends) and keys_ok:
    print("[ok] validation passed")
    raise SystemExit(0)
print("[fail] invalid or mismatched fences/keys")
raise SystemExit(1)
