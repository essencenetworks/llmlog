---
title: "Home"
draft: false
---


**LLMLOG** is a tiny, portable convention for embedding project or session metadata directly inside LLM chat sessions.  
It works across all major generative AI products - ChatGPT, Claude, Gemini and others.

---

## Here's how you'd use it 


#### 1. **Write your first log entry**  
   In any chat window, type:
   ```text
   /llmlog "testing the llmlog convention"
   ``` 
   The chat system will respond:
```llmlog-meta   
LLMLOG/1.0 BEGIN project=tech-llm organisation=acme-corp date=2025-09-09T19:32:00+12:00 scope=meta IGNORE_META
entry:
  testing the llmlog convention
mission:
  
outcome:
  
LLMLOG/1.0 END
```
#### 2. **Add a mission and perhaps -  an outcome**
   Extend the log entry with a mission and outcome.
   ```text
   /llmlog "I'm cataloging this thread so I can find it later " mission="effective knowledge management"
   ```
   The chat system will repond:

```llmlog-meta   
LLMLOG/1.0 BEGIN project=tech-llm organisation=acme-corp date=2025-09-09T19:33:00+12:00 scope=meta IGNORE_META
entry:
  I'm cataloging this thread so I can find it later
mission:
  effective knowledge management
outcome:
  
LLMLOG/1.0 END
```

#### 3. **And so on..** - layer on more context as you move through chat sessions and threads

#### 4. Keep it portable
Save the plain text in repos, your personal filing system, notes, or knowledge bases.
Works in ChatGPT, Claude, Gemini, and others.

---
## How to Install

LLMLOG works by issuing a simple *controller text message* in your chat session 
>Think of it as a set of house rules: it tells the AI when to notice a log line and how to format it.  

You don’t need special software — just copy the controller text into your own AI (ChatGPT, Claude, Gemini, other).  

→ [Copy the controller text from llmlog-controller.txt](https://github.com/essencenetworks/llmlog/blob/main/controller/llmlog-controller.txt) 

→ Paste it in your AI's chat window and press **Enter**

→ Your AI will repond:
```text
Controller registered. Awaiting /llmlog commands.
```




## Next Steps

- **Read the spec** → see the [README on GitHub](https://github.com/essencenetworks/llmlog)
- **Join the discussion** → [GitHub Discussions](https://github.com/essencenetworks/llmlog/discussions)
- **Examples** → browse the [examples directory](https://github.com/essencenetworks/llmlog/tree/main/examples)
- **Controller reference** → [llmlog-controller.txt](https://github.com/essencenetworks/llmlog/blob/main/controller/llmlog-controller.txt)

---

*LLMLOG is designed to stay simple: one line of text is enough to capture useful context.*
