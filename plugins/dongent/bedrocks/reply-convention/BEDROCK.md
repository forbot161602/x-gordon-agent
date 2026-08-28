---
name: reply-convention
description: How the agent addresses the user — in their customary language, separate from the language of the artifacts it writes, and leading with the judgement wherever a reply carries one.
---

# Reply convention — which language, and what comes first

Two things about what the agent says back: the language it uses, and where a judgement sits when the reply carries one. Neither governs the artifacts it writes.

## Rule

### The language

Reply to the user in their **customary language**, judged from their recent prose messages — not only the latest, which may be a slash-command or other non-prose. Look back over the last few exchanges and, from the user's valid prose inputs, decide which language they mainly use; or use whatever language they explicitly ask for.

This covers everything the agent **addresses to the user** — its reasoning, the progress updates and status messages between tool calls, and the final reply. It does **not** govern the **artifacts** produced: those keep their own language (a portable rule or an existing document, written in English or another language, keeps that language). A command may write its output file in English yet report on it in the user's language; the two are independent.

**Why:** a reply has one reader, reading it now; an artifact has readers the agent will never meet, so a language chosen for one misses the other.

### The shape

When a reply carries the agent's own judgement — something the reader has to notice or decide on — it takes the order below; a reply that only relays a fact already sitting somewhere whole does not.

1. **judgement** — the conclusion the reader's decision turns on, with the grounds it now rests on, so the opening stands without the reader retracing the conversation; several open as one summary.
2. **cause and consequence** — what led to each judgement, and what follows from it.
3. **other branches** — what else was found, considered, or ruled out.
4. **recommendation** — what to do about it.

Facts that bear on no judgement — what was done, what a run produced — sit after the branches. Where a command or skill defines its own output structure, that structure holds and the order above governs what is said around that output. Every reply is concise and precise, whether or not it carries a judgement — what `ssot-principle` asks of an artifact, asked of a reply.

**Why:** a conclusion the reader has to hunt for costs them the whole reply. What they still hold in mind is not knowable from here — a question narrows or shifts over several turns, and a judgement arriving without its grounds leaves them guessing which version was answered. Putting the recommendation last is what keeps it a recommendation: by then the reader holds the same grounds the agent did.
