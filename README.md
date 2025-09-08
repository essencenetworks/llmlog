<img src="llmlog_banner_trek_1200x630.png" alt="LLMLOG" width="100%">

# LLMLOG — Front‑matter for Chats (Spec 1.0)

**LLMLOG** is a tiny, portable convention for embedding **project/session metadata** directly **inside chat transcripts**.
It’s the simplest way to keep context with your conversations so exports remain searchable, groupable, and auditable.

- Works in any LLM UI (ChatGPT, Claude, Gemini…) with a one‑time controller
- Human‑readable & writeable (no tooling required)
- Machine‑parsable (regex‑friendly; ignores unknown keys)
- Token‑light (minimal formats; brief/minimal variants)

---
> **Name note:** This is the LLMLOG/1.0 spec + controller; unrelated to similarly named repos (e.g. XinTT/LLMLog).
---

## Quick start — LLM‑first capture

**Install the controller** (plain-text, safest)
	1.	Open controller/llmlog-controller.txt (raw).
	2.	Copy everything.
	3.	Paste into your chat app’s custom/system instructions (or the very first message of a new chat).
	4.	Test with: /llmlog "hello world"

> Tip: copy from the plain-text file to avoid Markdown fencing issues.

Now use it:
```
/llmlog "making progress with prompt design today"
/llmlog "design session with gpt5 on the logging mechanism" mission="effective knowledge management" tags=prompting,design
```

### Memory & persistence (FYI)
Some UIs (e.g., ChatGPT) may auto‑save “controller‑like” text to personal **Memory**. If you prefer session‑only behavior:
- Use temporary/incognito chats, or toggle Memory off while using `/llmlog`.
- Avoid phrases like “always / from now on / remember” in the controller.
- If a memory is created, delete it in the app settings. The controller is intended to be session‑local.

---

## Spec summary (1.0)

- Fence: `LLMLOG/<version> BEGIN …` / `LLMLOG/<version> END`
- BEGIN requires: `project=`, `date=`, and `organisation=` (alias `organization=`)
- Optional on BEGIN: `tags=tag1,tag2` (CSV; lowercase; no spaces). Alias: `tag=<single>`
- Recommended: `scope=meta` and `IGNORE_META`
- Body labels: `entry:`, `mission:`, `outcome:` (free‑form; optional)
- Parsers ignore unknown keys and should normalise `organization`→`organisation` and split `tags` to a list
- See **SPEC.md** for normative language and edge cases.

---

## Examples

See **examples/** folder, including:
- `example-entry-only.md`
- `example-entry-mission.md`
- `example-with-tags.md`
- `example-minimal.md`
- `example-us-organization.md`

---

## Tools (optional)

To keep the core minimal, tools are **illustrative** only:

- `tools/llmlog_parse.py` — reads a file/stdin and emits JSON Lines (one object per block)
- `tools/llmlog_validate.py` — strict fence/keys check (exit 0/1)
- `tools/llmlog_gen.py` - generate a deterministic block (LLMs can occasionally drift)

You can adapt these to your stack or write your own in any language.

---

## Related work (snapshot)

- **In‑app workspaces** (e.g., ChatGPT Projects): good UI containers, but metadata lives outside message text.
- **Post‑export scripts**: convert `conversations.json` to Markdown with front‑matter (adds metadata after the fact).
- **Prompt files w/ YAML front‑matter** (`.prompty`, dotprompt): great for **files**, not **chats**.
- **LLMOps observability** (LangSmith/Helicone/Humanloop): app‑level logging, not user conversational provenance.

LLMLOG applies “front‑matter” to conversational text so provenance is portable across vendors and time.

---

## Contributing

Keep 1.0 tiny and stable. Changes should be backwards‑compatible and motivated by real usage.  
Open an issue with examples and proposed text; small PRs welcome.

**Canonical repo:** https://github.com/essencenetworks/llmlog

## Contact

- Bugs / features: please open a [GitHub Issue](../../issues/new/choose).
- Questions / ideas: use [GitHub Discussions](../../discussions).
- Security reports: see [Security policy](.github/SECURITY.md).
- Contributing: see [CONTRIBUTING.md](CONTRIBUTING.md). SLA: best effort.
- Web: https://essencenetworks.com



---

## License

MIT License. Copyright (c) 2025 Essence Networks Limited — https://essencenetworks.com
