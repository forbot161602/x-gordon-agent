---
name: reply-language
description: Which language the agent addresses the user in — their customary language, separate from the language of the artifacts it writes.
---

# Reply language

The language the agent addresses the user in — separate from the language it writes artifacts in.

## Rule

Reply to the user in their **customary language**, judged from their recent prose messages — not only the latest, which may be a slash-command or other non-prose. Look back over the last few exchanges and, from the user's valid prose inputs, decide which language they mainly use; or use whatever language they explicitly ask for.

This covers everything the agent **addresses to the user** — its reasoning, the progress updates and status messages between tool calls, and the final reply. It does **not** govern the **artifacts** produced: those keep their own language (a portable rule or an existing document, written in English or another language, keeps that language). A command may write its output file in English yet report on it in the user's language; the two are independent.
