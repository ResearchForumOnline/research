---
title: "Reversible Recursive Source Improvement with Candidate Isolation"
author: "Shafaet Brady Hussain"
date: 2026-09-27
status: "author-led engineering working paper"
license: "CC BY 4.0"
---

# Reversible Recursive Source Improvement with Candidate Isolation

**Shafaet Brady Hussain**
Independent researcher, ResearchForumOnline, United Kingdom
27 September 2026

## Abstract

An agent that can edit its own application source should not equate a passing check with a safe or better successor. I describe the candidate-isolation design in TalkToAi Code's Skynet Mode: a frozen source snapshot, bounded proposed changes in a disposable candidate, unchanged check files, optional metric evaluation, reviewable diff, checked application to the original project and hash-guarded restore. The system supports recursive *source* improvement proposals; it does not rewrite the served model's weights or make ethics code physically immutable. I state the invariants needed for a scientifically meaningful improvement claim and give an evaluation design that can detect reward hacking, scope drift and stale baselines.

## 1. Why recursion needs a boundary

“Improve yourself” conflates at least three activities: edit application code, tune configuration, and train model weights. They have different risk and evidence requirements. The released workflow addresses the first. A candidate branch or copy is an experiment on source code; a model-weight rewrite would require a training dataset, rights review, compute, independent holdout and a deployment gate outside this workflow.

Let a candidate be `C_i = F_i(B, G, E)`, where `B` is frozen baseline source, `G` a stated goal, and `E` permitted evidence. To claim an improvement, the evaluation `M(C_i)` must be fixed before candidate generation, independent of mutable test code, and interpreted alongside regressions and resource cost. Passing a build establishes compatibility with that build, not strict improvement in gameplay, safety or intelligence.

## 2. Source workflow

The public [TalkToAi 8.0 source ledger](../sources/talktoai-code-8-evidence-ledger.md) pins `skynet_mode.py` and `candidate_apply.py`. The workflow runs a bounded number of candidate iterations in a disposable project copy. Protected policy files and frozen check files are compared before accepting a candidate. Without a configured evaluator, the workflow may retain the latest candidate that passed checks; that state must be called *checks passed*, not *quality improved*. With an explicit frozen evaluator contract, selection requires a finite metric strictly better than the baseline or previous best, in addition to passing checks. Even then the measured metric is only a proxy for the declared goal.

Application to the real project is a separate step. The candidate and original file hashes are rechecked, original bytes are backed up, and an application manifest records what changed. Restore verifies that the applied files have not since been edited, to avoid overwriting later user work. Source changes produced by other tools can invalidate earlier verification. These mechanisms form a transactional pattern but do not provide a database-style atomicity guarantee for every possible crash or external process.

## 3. Evidence and limits

The frozen release's tests exercise candidate controls, change detection and executable-mode preservation across platforms. A historical CI failure on commit `b5b283c` exposed a test-fixture error: the fixture changed a POSIX executable mode without updating its saved baseline. The one-line correction on commit `e5dcf58` and subsequent Ubuntu/macOS passing runs show why negative evidence should remain visible rather than be erased from a release narrative. The latest 8.0 run passed on both platforms. None of these receipts proves that generated candidates improve arbitrary projects.

The user's earlier Probability of Goodness research argues for separating a score from action authority. That separation applies here: a scalar evaluator should rank eligible candidates only after hard constraints, frozen checks and permission rules. A high metric must not authorize reading credentials, altering held-out tests or publishing a release. This paper does not claim a calibrated ethical probability.

## 4. Falsifiable invariants

1. A candidate that modifies frozen checks or protected policy must be rejected before its reported score can select it.
2. A candidate whose metric is `NaN`, infinite, missing or no better than baseline must not receive an improvement label.
3. A changed original file hash between evaluation and application must stop application without overwriting that file.
4. Restore must stop when an applied file has subsequently changed.
5. The evaluation report must distinguish checks-only selection from metric improvement and must retain failures.

These are local software invariants. They do not imply the policy is uneditable by an operating-system administrator or that the surrounding application is attack-proof.

## 5. Evaluation design

To compare recursive and single-pass coding fairly, assemble a rights-cleared suite of projects with fixed source snapshots, hidden behavioral tests, static checks and a measured user outcome. Give both conditions the same model, wall-clock, token and tool budget. Freeze evaluator and hidden tests before trials; make the candidate unable to edit them. Report generated candidates, rejected candidates, applied changes, hidden-test performance, regressions, restore failures, and human review findings. A useful ablation removes hash guarding to measure stale-application incidents in a controlled sandbox, not in user projects.

The falsifier is straightforward: if iterative candidates do not outperform one-shot edits on held-out outcomes after equal budget, or if they increase destructive regressions, the claimed benefit fails. Iteration count itself is not an intelligence metric.

## 6. Conclusion

Recursive source improvement can be treated as a sequence of bounded, reversible experiments. The release implements candidate isolation and review gates, while leaving model-weight training and any strong AGI claim outside its evidence. A future benchmark should test whether the extra passes produce measurable value per unit cost without compromising user work.

## AI-use and conflict disclosure

AI tools assisted source inspection, drafting and editing. I take responsibility for this author-led paper and am associated with the evaluated software. It is neither independent validation nor peer review.

## References

1. ResearchForumOnline, [TalkToAi Code 8.0 source and release](https://github.com/ResearchForumOnline/TalkToAi-Code/tree/047a6a44914df8e16509aa6f4334e69ba999502c), 2026.
2. Shafaet Brady Hussain, [Probability of Goodness Decision Routing 1.0](probability-of-goodness-ethical-routing.md), 2026.
3. [TalkToAi Code 8.0 evidence ledger](../sources/talktoai-code-8-evidence-ledger.md).
