---
title: "Outcome-First Task Navigation for Local and Self-Hosted Coding Agents"
author: "Shafaet Brady Hussain"
date: 2026-09-27
status: "author-led engineering working paper"
license: "CC BY 4.0"
---

# Outcome-First Task Navigation for Local and Self-Hosted Coding Agents

**Shafaet Brady Hussain**  
Independent researcher, ResearchForumOnline, United Kingdom  
27 September 2026

## Abstract

I examine a practical obstacle in local coding agents: users describe an outcome, while the application expects them to choose a workspace, locate a model, discover tools and decide when to browse. TalkToAi Code 8.0 adds a deterministic preflight for two common requests. A request to find a Desktop project triggers a bounded manifest scan of Desktop and Documents. A relevant game, website or application task can trigger a fixed-topic search of public documentation before model generation. The search query does not interpolate the user's prompt, path or credentials; the word `offline` and related phrases suppress it. The agent receives source observations and can still use its ordinary tools. This is an implemented usability hypothesis, not a measured improvement in task-completion rate. The paper provides an inspectable architecture, failure modes and a controlled evaluation protocol.

## 1. Problem and research question

A local model can have file, browser and server tools yet fail to use them if tool discovery consumes too much context or the user does not know which tool to request. The relevant research question is narrower than “Can the system do everything?”: **Can a small deterministic preflight reduce user configuration burden without silently increasing data exposure or pretending that a source lead is verified knowledge?**

The unit of analysis is the coding-agent turn. An outcome request enters the app, a selected project and access settings define scope, and the controller may perform a bounded read-only preflight before the model begins. Project editing still requires Act mode and the existing tool permissions. An OpenSSH alias does not become a connection merely because its name was discovered.

## 2. Implemented method

The frozen [8.0 source snapshot](../sources/talktoai-code-8-evidence-ledger.md) defines `research_query(request, engine)` as a small classifier. It recognizes build/current-language patterns and game, web or application topics. It returns one of a finite set of public-documentation queries; no function concatenates the original request or project path into that query. Explicit offline language returns no query. The controller records the search in its tool activity, filters source links to designated primary documentation hosts, and attempts to open a canonical primary page. A failed web step reports failure and leaves project tools available.

`desktop_projects` enumerates project markers such as `project.godot`, `package.json` or `pyproject.toml`. It does not read the contents of those files. The scan avoids symlinks and excluded directories, has depth, count and time bounds, and reports its scope. This discovery metadata can help the model ask which project the user meant; it is not an automatic authorization to edit every folder found.

The UI adds plain-language examples and starters. This is interface scaffolding rather than a claim that the model understands all natural language. Task starters fill a request; they do not execute tools simply by being selected.

## 3. Observable evidence and negative space

The unit tests cover generic-query non-disclosure of a synthetic path and password string, offline opt-out, a simple local edit that triggers no research, canonical-source selection, and exclusion of a synthetic secret folder. They are deterministic specification checks, not a study of user privacy or model behavior. The public Ubuntu/macOS workflow passed installation, offscreen launch and its listed agent regressions on commit `047a6a4`; the Windows release has a published installer digest. These receipts do not establish that the preflight improves completed-game quality.

A direct Godot stable-docs page is used because a search engine may return redirect links instead of clean original URLs. Opening that page establishes a current source observation, not a universal fact about the user's game. The agent must still compare documentation with the detected engine version and inspect local files before changes.

## 4. Threat model

Four failures matter. First, a classifier can choose the wrong subject and waste time or model context. Second, a public search still reveals the generic subject and the user's network address to the search service. Third, path names from Desktop discovery may enter the selected inference provider's context; when that provider is remote, those names can leave the machine. Fourth, a retrieved page can contain misleading text or prompt injection. The controller therefore uses fixed queries and bounded observations, while the agent prompt treats page content as untrusted data. Neither mechanism is a formal noninterference proof.

The preflight also adds latency. A slow browser or blocked search must remain visible and should not make local coding unavailable. Future releases should measure p50/p95 preflight latency and report the fraction of queries producing an opened primary source.

## 5. Falsifiable evaluation protocol

I propose a preregistered paired task set of novice requests for existing Godot, Python and web projects, plus deliberately ambiguous and offline requests. Hold model, hardware, project snapshot, time budget and tool permissions fixed. Randomize preflight enabled/disabled order across tasks. Record: correct project identification, sensitive-string presence in outbound search queries, elapsed time to first useful tool observation, verified task completion, unnecessary external calls, and user interventions. Inspect network traces for query leakage. Use independent reviewers to score outcomes from project files and checks, not from the model's own “done” message.

The null hypothesis is that preflight does not improve verified task completion or reduce user intervention. A privacy gate fails if any canary path or credential substring appears in an automatic query. A successful test must report failures and latency costs as well as gains.

## 6. Conclusion

Outcome-first routing is a limited systems intervention: move a small amount of predictable discovery before generation while keeping tool authority and verification explicit. It is useful only if measured completion improves and its privacy and latency costs remain acceptable. The current release establishes an inspectable implementation and regression baseline, not that empirical conclusion.

## AI-use and conflict disclosure

AI tools assisted source inspection, drafting and editing. I take responsibility for the research framing and release decisions. I am associated with the evaluated TalkToAi project; this is an author-led evaluation, not independent validation or peer review.

## References

1. ResearchForumOnline, [TalkToAi Code 8.0 frozen source and release](https://github.com/ResearchForumOnline/TalkToAi-Code/tree/047a6a44914df8e16509aa6f4334e69ba999502c), 2026.
2. Godot Engine, [Optimizing 3D performance](https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html), stable documentation.
3. [TalkToAi Code 8.0 evidence ledger](../sources/talktoai-code-8-evidence-ledger.md).
