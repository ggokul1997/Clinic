# ai-lab — MERN → AI Engineer

A working lab, not a syllabus. Each build ships a real piece of the Clinic
subagent ecosystem and teaches one competency. Code first; theory when you hit it.

## Ground rule

Everything here is **learning code**. `PROJECT_BRIEF.md` says the project is still
in strategic research, so nothing in `ai-lab/` goes near the production path until
we deliberately promote it.

## The six builds

| # | Build | Ships toward | New competency | Status |
|---|-------|--------------|----------------|--------|
| 1 | Structured extraction + eval harness | Competitor Intelligence Agent | Schema-constrained output, provenance, **evals** | ← you are here |
| 2 | Retrieval over clinic content | Front-Desk Agent | Chunking, embeddings, hybrid search, reranking | |
| 3 | Tool-calling agent | Booking Agent | Tool design, the agent loop, failure recovery | |
| 4 | Autonomous multi-step loop | Competitor Intelligence Agent (full) | Planning, termination, context engineering | |
| 5 | Orchestration + observability | Subagent ecosystem | Multi-agent handoff, tracing, cost/latency ops | |
| 6 | Hardening | All of it | Prompt injection, PII, output validation, fallbacks | |

## What your MERN background already covers

Roughly half this job. You already own: HTTP/API design, async and concurrency,
streaming to a client (SSE is how token streaming reaches React), queues and
background jobs, schema design, auth, caching, deployment, observability plumbing.
An LLM call is just a slow, expensive, non-deterministic HTTP request.

## The one thing that is genuinely new

**Non-determinism.** Every instinct you have about testing assumes the same input
gives the same output. It doesn't here. `assert result === expected` is dead, and
what replaces it — evals — is the actual skill that separates AI engineers from
people who can call an API. That's why Build 1 is an eval harness and not a chatbot.

## Setup

```bash
pip install -r ai-lab/requirements.txt
```

Auth: run `ant auth login`, or export `ANTHROPIC_API_KEY`. The SDK finds either
one on its own — don't pass a key in code.
