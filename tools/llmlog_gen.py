# tools/llmlog_gen.py
import re, sys, datetime, argparse
rx = re.compile(r'[^A-Za-z0-9._-]')
def norm(s): return rx.sub('-', s).lower()
p = argparse.ArgumentParser()
p.add_argument("entry")
p.add_argument("--project", default="tech-llm")
p.add_argument("--org", default="essencenetworks")
p.add_argument("--mission", default="")
p.add_argument("--outcome", default="")
p.add_argument("--tags", default="")
p.add_argument("--date", default=datetime.datetime.now().astimezone().isoformat())
a = p.parse_args()
tags = ",".join({t.strip().lower() for t in a.tags.split(",") if t.strip()}) if a.tags else ""
begin = f"LLMLOG/1.0 BEGIN project={norm(a.project)} organisation={norm(a.org)} date={a.date} scope=meta IGNORE_META"
if tags: begin += f" tags={tags}"
print("```llmlog-meta")
print(begin)
print("entry:\n  " + a.entry.strip())
print("mission:\n  " + a.mission.strip())
print("outcome:\n  " + a.outcome.strip())
print("LLMLOG/1.0 END")
print("```")
