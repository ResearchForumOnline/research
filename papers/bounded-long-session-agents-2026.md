---
title: "Bounded Continuation and Progress Evidence in Long-Session Coding Agents"
author: "Shafaet Brady Hussain"
date: 2026-09-27
status: "author-led engineering working paper"
license: "CC BY 4.0"
---

# Bounded Continuation and Progress Evidence in Long-Session Coding Agents

**Shafaet Brady Hussain**  
Independent researcher, ResearchForumOnline, United Kingdom  
27 September 2026

## Abstract

“Keep going” is an attractive instruction for coding agents but is not, by itself, an execution policy. A local model may spend its budget rereading the same files, lose the original objective during context condensation, repeat a failed command, or assert completion after a build starts but before it exits. I describe the bounded-continuation design in TalkToAi Code: work-session ceilings, compact task goals, repeated-discovery detection, managed process polling, workspace-change observations and verification-state invalidation. This is an architecture and source-evidence paper. It does not claim that a prompt alone improves intelligence or that a selected four-hour ceiling guarantees four hours of productive work.

## 1. Research question

How can a coding agent continue over multiple local-model responses while retaining an auditable distinction between *activity*, *progress* and *verified completion*? These terms are operationally different. Reading the same directory three times is activity; discovering a previously unknown entry can be progress; a passing unchanged project check after the final edit is one kind of verification. No single counter captures all three.

The design objective is to make a long session interruptible and recoverable without treating a self-reported checklist as evidence. The agent can steer or stop, but work already delivered to external tools is not undone by a Stop press.

## 2. Controller model

Let a session state be `S = (G, H, T, W, V, B)`, where `G` is the current goal and acceptance criteria, `H` the compacted conversation/history, `T` the available tool set and tool observations, `W` the observed workspace revision, `V` verification status, and `B` the remaining step/time budget. A continuation is admissible only while the user has not stopped it, the ceiling remains, and the controller has not detected an unproductive or unresolved-error loop.

In the frozen TalkToAi Code source, a requested work-session duration is clamped to at most 240 minutes and, if nonzero, at least 15 minutes. Longer sessions allow up to twelve bounded passes of the selected per-pass step budget. A separate time deadline can stop the turn sooner. These are maximums, not expected run lengths. Task goals record an objective, criterion states and a next action; they are model reports. Tool and workspace evidence must support a claim that a criterion was met.

The progress guard records signatures of repeated discovery calls. It can pause a pattern of unchanged listings and ask the agent to change strategy. Managed process jobs can run a build or test without blocking the interface, but a job in `running` state is not a pass. The agent must poll for exit and inspect logs. Workspace change tracking observes a bounded source subset. A changed revision marks earlier verification stale; an incomplete scan cannot rule out changes elsewhere.

## 3. Evidence from the release snapshot

The public [source ledger](../sources/talktoai-code-8-evidence-ledger.md) binds `agent_core.py`, `progress_guard.py` and `workspace_change_evidence.py` to SHA-256 values and commit `047a6a4`. The public cross-platform smoke workflow passed its declared tests. Author-led Windows source tests reported 429 cases, 12 skipped. Those totals cover a heterogeneous codebase and must not be converted into a reliability percentage for long autonomous projects.

The UI exposes elapsed time, model step and tool activity so that a slow local model is not mistaken for an idle app. This visibility is necessary but insufficient: a continuous token stream can still be unproductive. In one previously documented disposable fixture, the configured 30B server model ran roughly 258 seconds over eight tool steps, changed one source file, passed two existing tests, saved a playbook and paused at its step limit. The fixture is a case observation, not evidence of general game-scale autonomy.

## 4. Failure cases and invariants

Four invariants should hold. First, after a changed source revision, `passed` must not remain the current verification state. Second, a repeated unchanged discovery sequence should not consume the whole long-session budget without a visible recovery or pause. Third, a task goal should preserve unmet criteria across an ordinary Continue request. Fourth, a cancelled or timed-out job must not be labelled completed. Counterexamples should be included in regression tests.

The architecture cannot ensure global progress. The scan has explicit bounds; a shell command may alter files outside it. Context condensation can omit a detail the model later needs. A model may report an incorrect goal state. “Keep going” therefore remains conditional on new observations and checkable criteria, with a visible pause report when the conditions fail.

## 5. Proposed comparative study

A meaningful experiment would freeze ten to twenty multi-file issues with known acceptance tests, record the same model, context size, tools and hardware, then compare: single-pass; naive repeated “continue”; and bounded continuation. Outcomes should include issue completion judged by hidden tests and human review, redundant tool calls, stale-verification claims, wall-clock and token cost, and number of user interventions. Each issue should run from a clean snapshot with a fixed time and step budget. Long tasks that produce no final answer remain failures or censored observations, not silent successes.

## 6. Conclusion

Long-running agency is an engineering discipline of budgets, state, evidence and interruption. The released controller implements these mechanisms in a bounded way. The next research step is controlled task-level comparison against naive continuation, including negative cases and resource costs.

## AI-use and conflict disclosure

AI tools assisted source inspection, drafting and editing. I take responsibility for this author-led analysis. I am associated with the evaluated software. No independent peer review or universal task-completion result is claimed.

## References

1. ResearchForumOnline, [TalkToAi Code 8.0 source](https://github.com/ResearchForumOnline/TalkToAi-Code/tree/047a6a44914df8e16509aa6f4334e69ba999502c), 2026.
2. [TalkToAi Code 8.0 evidence ledger](../sources/talktoai-code-8-evidence-ledger.md).
3. W3C, [PROV Overview](https://www.w3.org/TR/prov-overview/), 2013. Used as conceptual background on traceability; no full PROV conformance is claimed.
