# LLMLOG/1.0 — Specification (format-only)

**Status:** Stable. This document defines the on‑text serialization for **LLMLOG/1.0** (“front‑matter for chats”).  
**Scope:** Wire/markup format only. Implementation details (LLM controllers, UI behavior, validators) are **non‑normative** and live outside this spec.

For a reference controller (informative), see: `controller/llmlog-controller.txt`.

---

## 1. Goals (informative)
- **Portable:** metadata travels with transcripts (copy/paste, export).
- **Minimal:** BEGIN/END fences, a few `key=value` tokens, and three optional body fields.
- **Predictable:** easy to parse with simple, line‑oriented tooling.

## 2. Non‑goals (informative)
- Inference of intent or instruction of models.
- Access control, security, or identity semantics.
- UI/agent/controller behavior (kept in companion docs).

---

## 3. Block structure (normative)

A conformant block has a BEGIN fence, an optional body, and an END fence:

```
LLMLOG/1.0 BEGIN project=<PROJECT> organisation=<ORG> date=<TIMESTAMP> [tags=t1,t2,...] [other-keys]
entry:
  <free text>
mission:
  <free text or blank>
outcome:
  <free text or blank>
LLMLOG/1.0 END
```

- The block **begins** with `LLMLOG/<major.minor> BEGIN …` and **ends** with `LLMLOG/<major.minor> END`, each on its own line.
- The **BEGIN** line is a sequence of **space‑separated** `key=value` tokens; token order is not significant.
- **Required BEGIN keys:** `project=`, `date=`, and one of `organisation=` | `organization=` (alias). Consumers **SHOULD** normalise `organization` → `organisation` internally.
- **Optional BEGIN keys:** `tags=<csv>` (alias: `tag=<single>`). Consumers **SHOULD** split on commas and **MAY** normalise case.
- **Unknown BEGIN keys:** Consumers **MUST** ignore unknown keys so blocks remain forward‑compatible.

### 3.1 BEGIN value grammar (normative)
- The BEGIN line is a sequence of space-separated `key=value` tokens.
- The `value` portion of each token MUST NOT contain whitespace (space, tab, newline).
- This specification places no other constraints on characters in values.

### 3.2 Body fields (normative)
- The ONLY valid body labels in **LLMLOG/1.0** are: `entry:`, `mission:`, `outcome:`.
- After a label and its colon, a **newline MUST follow**. The field value begins on the next line and may span multiple lines until the next label or END.
- Body fields are **optional**; empty values are allowed.
- Any other body label (e.g., `tags:` or `notes:`) renders the block **non‑conformant**.

### 3.3 Tags location (normative)
- `tags` MUST appear **only** on the BEGIN line as `tags=<csv>` (alias: `tag=<single>`).
- A body section `tags:` is **invalid** in **LLMLOG/1.0**.

### 3.4 Timestamp (informative)
- `date=` is commonly ISO‑8601 with local offset (e.g., `2025-09-06T09:00:00+05:30`); other formats are permitted by implementations, but ISO‑8601 is **RECOMMENDED**.

---

## 4. Conformance (normative)
- **Producer conformance:** MUST emit valid fences; MUST include required BEGIN keys; MUST place `tags` on BEGIN only; MUST avoid whitespace in values.
- **Consumer conformance:** MUST accept the `organization` alias; MUST ignore unknown BEGIN keys; SHOULD parse `tags` as a list split on commas; SHOULD treat body text as opaque UTF‑8.

---

## 5. Examples (informative)

**Entry only**
```llmlog-meta
LLMLOG/1.0 BEGIN project=tech-llm organisation=essencenetworks date=2025-09-06T09:00:00+05:30
entry:
  making progress with prompt design today
mission:

outcome:

LLMLOG/1.0 END
```

**Entry + mission + tags**
```llmlog-meta
LLMLOG/1.0 BEGIN project=tech-llm organisation=essencenetworks date=2025-09-06T09:05:00+05:30 tags=prompting,design,paper
entry:
  design session with gpt5 on the logging mechanism
mission:
  effective knowledge management
outcome:

LLMLOG/1.0 END
```

**US spelling (alias)**
```llmlog-meta
LLMLOG/1.0 BEGIN project=site-redesign organization=acme date=2025-09-06T09:15:00+05:30 tags=retrospective
entry:
  kickoff
mission:

outcome:

LLMLOG/1.0 END
```

---

## 6. Versioning (normative)
- This document defines **LLMLOG/1.0**.
- Minor revisions MAY add optional keys or clarifications that remain backward‑compatible.
- Major revisions (e.g., `2.0`) may change semantics and MUST use corresponding fences (`LLMLOG/2.0`).

## 7. License
---
CC BY 4.0 © 2025 Essence Networks Limited — https://creativecommons.org/licenses/by/4.0/  
Please attribute as “LLMLOG/1.0 — Specification” (Essence Networks Limited), include a link to the source, and note changes.