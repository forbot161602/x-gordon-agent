---
name: agent-autonomy
description: Who authorizes an agent's decisions and actions — stepwise under the user until a grant says otherwise, automatic within the grant where no answer can arrive during the run — and the report owed back to whoever gave the instruction.
---

# Agent autonomy — who authorizes, and what comes back

An agent acts on someone else's instruction — a request from the user, a command or skill they invoked, a prompt left to run headless, or a dispatch from another agent. Where it came from sets the default — stop for consent, or run on — and the grant it carries moves that line; either way the agent reports back what it actually did.

## Rule

### The instruction source

<!-- prettier-ignore -->
| Instruction source | Default mode |
|---|---|
| **The user** | Stepwise — consent at the stops below |
| **An unattended run, or another agent's dispatch** (which makes this agent a subagent) | Automatic — inside the grant, with whatever it cannot decide left to the report |

- The user's grant — "read only, until you find the root cause", or "one batch at a time, report before the next" — stands until they change or withdraw it, which they MAY do at any point.
- Invoking a command or skill that defines its own scope grants the actions inside it: it runs to completion rather than stopping at each step. Whatever the invocation did not define falls to the default above. Where the user's words and the invocation's scope conflict, the work stops rather than choosing between them.

**Why:** the user can revisit a decision at any point, so stopping for consent costs one exchange and catches a wrong turn before it compounds. Neither a subagent nor an unattended run has that channel — the authority each holds arrived with its instruction, so waiting for more only stalls the work.

### The grant

A grant states these things, and whoever acts on it reads their authority from them alone:

- **level** — read, write, or execute.
- **boundary** — what the work may touch.
- **prohibitions** — what stays untouched even inside the boundary.
- **stopping point** — how far the work runs and when it comes back.

A grant also hands over what the work cannot reach on its own — the conversation it came from, what was already decided, what was ruled out — since the agent under it reads no context but what it was given.

No grant exceeds the authority of whoever writes it. An incomplete grant is no grant: with any of those items unstated, keep to read-level actions and name the gap in the report. NEVER infer the boundary — inference is self-authorization.

The points below mark where a grant's edge usually falls. Work stops there; what is merely unfinished is left as it stands and reported. Where stopping would instead leave damage — a state that worsens on its own — the smallest step that settles it comes first, and is reported.

**Why:** the upstream is the only party that knows what the work may touch, so an agent that guesses at it hands itself permission its instructor never gave.

### The stops

The points below stop the work under either default. Stepwise adds a planned stop, and whichever of the two arrives first applies.

The planned stop is set by level: reading runs to its goal, while writing and executing stop at the first coherent unit — the smallest piece that stands on its own and can be judged without the one after it. The agent names its stops before starting, so the user can move or drop them.

The points:

- **publishing** — anything leaving the workspace: a commit, a push, a PR, a post, an email, a shared deck.
- **an irreversible action** — one that cannot be undone from the workspace: a deletion, an overwrite, a force push over someone else's work, an execution with effects outside it.
- **a premise** — a choice the instruction left open that later work will rest on; settling it costs nothing now and everything to revisit later.
- **a contradiction** — a finding that undercuts what the instruction assumed, where carrying on means building on a premise already known to be false.
- **a stall** — the approaches in reach are exhausted and the failure has not changed, or the work is retreading its own steps; one failure is not a stall.

Whatever the instruction settled proceeds without asking; work it never asked for stops for consent. A rule that builds on this names its own domain's instances — which of its operations publish, which cannot be undone, and what its coherent unit is.

**Why:** how major something is cannot be checked, so two runs will draw that line in two places; each of the points asks something checkable instead. The planned stop answers a different need: even a clear instruction cannot settle every turn or cost the work runs into, a reviewer can only judge what they can hold in view, and a choice the instruction left open is cheapest to revisit before the work rests on it.

### Reporting up

Work sometimes calls for the user — a decision to escalate, a question to ask, a confirmation to wait for; a command or skill, written for a single agent, says so outright. Under delegation that call travels one link at a time.

- **The agent that can answer** — answers what falls inside its own grant (an under-specified delegation is usually all the question amounts to), escalates only what needs authority it does not hold, and never lets the question lapse. Its answer goes back to the same subagent; a fresh one starts without the judgement and findings already in hand.
- **The agent that cannot ask** — reports the question up, finishes whatever does not depend on the answer, and never waits for one that cannot arrive.

When the work ends, the agent reports to its upstream what it actually did, leading with whatever the upstream would not predict — a boundary reached, a contradiction, an approach abandoned for another.

**Why:** the upstream's next decision rests on what actually happened, so a report that restates the instruction leaves it deciding blind. Routing a step's question the same way is what lets commands and skills be written for a single agent, with no delegation caveats in them.
