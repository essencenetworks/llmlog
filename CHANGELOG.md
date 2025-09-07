# Changelog

## 1.0.1 — 2025-09-06
- Add optional `tags` key on BEGIN line (CSV; lowercase; no spaces). Alias: `tag=`
- Update SPEC/README, examples, and example parser to parse `tags` into a list

## 1.0.0 — 2025‑09‑06
- Initial public baseline of **LLMLOG/1.0**
- Spec (SPEC.md), controller for `/llmlog`, examples
- Tiny parser (`examples/llmlog_parse.py`) and validator (`examples/llmlog_validate.py`)
