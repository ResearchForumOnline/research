---
title: "Tool-Protocol Reliability for Smaller Local Coding Models"
author: "Shafaet Brady Hussain"
date: 2026-09-27
status: "author-led engineering working paper"
license: "CC BY 4.0"
---

# Tool-Protocol Reliability for Smaller Local Coding Models

**Shafaet Brady Hussain**  
Independent researcher, ResearchForumOnline, United Kingdom  
27 September 2026

## Abstract

The observable failure in a coding agent is often not lack of code knowledge but a broken boundary between model text and executable tool calls. A model may print markup such as `<function=project_info>` in its answer, emit incomplete arguments, or repeat discovery after a tool result. I analyze the source-level reliability controls in TalkToAi Code: structured tool-call handling, bounded parsing of supported Qwen text forms, history repair that never retroactively executes saved protocol text, on-demand tool packs, and explicit observations before browser interaction. The paper proposes a protocol-fidelity benchmark that separates request recognition, valid call generation, execution, observation and final task correctness. Passing unit tests show implemented behavior at defined boundaries; they do not prove every local 30B or 27B model will call tools reliably.

## 1. Failure model

A coding agent crosses at least five boundaries: natural-language intent to selected capability; model output to a syntactically valid call; call to actual execution; returned observation to the next model state; and final answer to verified outcome. A failure at any one boundary can appear to the user as “the AI is thinking” while nothing happens to the project.

The screenshots that motivated this work showed tool markup appearing as text and a run that spent time listing source files. Those observations identify a protocol and progress problem, not a proof that a particular model is incapable of coding. A source-level fix must avoid the dangerous shortcut of executing any command-like text recovered from chat history: stored transcripts and external pages are untrusted content.

## 2. Implemented boundary controls

The frozen [source ledger](../sources/talktoai-code-8-evidence-ledger.md) identifies the controller, browser and tool-protocol files. The controller presents tool schemas to the model and receives tool calls through the model transport. For supported malformed text, a bounded parser can recognize complete Qwen-style calls during the current response; incomplete or ambiguous output is rejected rather than guessed. Saved assistant text containing apparent protocol syntax is repaired for the next model prompt as visible prose with an explicit statement that it was not executed. This prevents a historical transcript from gaining tool authority later.

Tool packs are discovered through an `enable_tools` catalog when context is scarce. The context budget can shed optional schemas while retaining essential project tools. This improves the chance that a small context window fits, but may add a discovery turn; it does not establish optimal tool choice. Task preflight in release 8.0 handles a small predictable subset before generation, including generic public-doc research and Desktop project discovery.

For browser action, the task-owned Playwright session observes an accessibility snapshot and returned URL. It requires an exact observed control for a click and rejects ambiguous matches. An action is followed by another observation. Playwright's Python API documents the accessibility snapshot primitive; the application-specific authority rule comes from TalkToAi's code, not from Playwright itself.

## 3. Measurement framework

I propose a benchmark with five separate denominators. `I` is the fraction of tasks for which the controller/model chooses the needed capability; `S` the fraction of attempted calls that validate against schema; `E` the fraction of validated calls that execute successfully; `O` the fraction whose returned observation is incorporated correctly; and `C` the fraction of end-to-end tasks whose requested outcome is independently verified. Multiplying these rates would require independence assumptions that are unlikely to hold. They should be reported separately, by model and task type, with raw counts.

Test fixtures should include complete native calls, complete text-form calls, truncated tags, malformed JSON, duplicated call IDs, tool-looking text inside a web page, and saved history containing a prior failed call. The expected behavior for tool-looking page text is data treatment, never execution. The expected behavior for an incomplete call is no side effect and a visible recovery path. Real model trials should distinguish parser repair from native model compliance.

## 4. Threats to validity

One successful model run cannot estimate protocol reliability. Unit tests may cover hand-authored cases that differ from model outputs in the field. Playwright accessibility snapshots depend on site markup and browser version; a successful snapshot is not an accessibility audit. Tool schema availability does not mean the app has permission for a remote host or private file. Most importantly, a valid `write_file` call can still make a poor edit. Final quality needs project tests and review beyond protocol fidelity.

## 5. Research contribution and next step

The contribution is a decomposition of agent reliability at the model-tool boundary, with a falsifiable measurement plan and an implemented controller case study. The next study should save a rights-cleared corpus of raw local-model responses under fixed prompts and versions, release a text-free structural trace, and compare parser variants without changing the task or tool authority. Report rejection rates as well as repaired-call success. Any claim of “ChatGPT-equivalent” ability would need a much broader blinded task comparison.

## AI-use and conflict disclosure

AI tools assisted inspection, drafting and editing. I take responsibility for this author-led analysis and am associated with TalkToAi Code. This is not independent validation or peer review.

## References

1. ResearchForumOnline, [TalkToAi Code 8.0 controller and protocol source](https://github.com/ResearchForumOnline/TalkToAi-Code/tree/047a6a44914df8e16509aa6f4334e69ba999502c), 2026.
2. Playwright, [Python Page API: `aria_snapshot`](https://playwright.dev/python/docs/api/class-page), accessed September 2026.
3. [TalkToAi Code 8.0 evidence ledger](../sources/talktoai-code-8-evidence-ledger.md).
