---
title: "OpenZero Model and Dataset Methodology 1.0"
author: "Shafaet Brady Hussain"
date: "2026-08-18"
license: "CC BY 4.0"
---

# OpenZero Model and Dataset Methodology 1.0
## Deterministic Curation, Prompt-Group Isolation, QLoRA Experiment Gates, and Evidence-Bounded Release

**Shafaet Brady Hussain**

Independent researcher and developer, United Kingdom

18 August 2026

## Abstract

I present an evidence-bounded methodology for constructing and evaluating small, local-first OpenZero language-model derivatives. The contribution is a reproducible process rather than a claim of a new foundation model. Three local conversational corpora containing 4,380 input rows were normalized, deduplicated, screened for a narrow class of credential-like strings, and divided by final-user-prompt groups. The resulting private research snapshot contains 2,743 accepted conversations: 2,606 training rows and 137 evaluation rows. Exact-conversation deduplication rejected 1,637 repeated rows. A deterministic seed and prompt-group split prevent identical final user prompts from appearing in both partitions. Five factory scripts compile successfully, but compilation is not training evidence. The proposed QLoRA path uses frozen 4-bit bases with low-rank adapters, requires exact base revisions, held-out evaluation, run manifests, and post-conversion inference before any derivative release. Qwen and Gemma specialists remain separate; a possible combined student is distillation from reviewed teacher pairs, not weight averaging. All source datasets and generated teacher outputs remain private because their composite licences are unresolved. No successful full specialist training, general capability improvement, safety certification, or public model release is claimed here.

## 1. Research question and contribution

The practical question is: how can a small independent project turn a mixed research corpus into auditable local-model experiments without confusing a runnable training script with a validated model? I answer with four linked controls:

1. deterministic normalization and row-level provenance;
2. group-aware train/evaluation isolation;
3. architecture-compatible adaptation and distillation boundaries; and
4. promotion gates that require hashes, comparisons, inference, licensing, and limitations.

The result is a methodology and reproducibility package. It does not establish that the resulting model is better than its base, safe for autonomous operation, or suitable for high-stakes use.

## 2. Corpus boundary

The private input snapshot comprised three English conversational datasets. Their public-safe identifiers, row counts, and exact file hashes are recorded below. The release omits the rows themselves, local paths, private evaluations, and provenance records that may contain third-party material.

| Source snapshot | Input rows | SHA-256 |
|---|---:|---|
| OpenZero Advanced Research v1 SFT | 361 | `d56b6f12036b537e6d97a2e8273eac5e7cc4b68a6019e5af0c1ae835961656d4` |
| OpenZero Zero Advanced v2 | 1,986 | `79a5235cefacb52dd67c368ec36d843c379fcc12aece5bedc400c5de7ff976a8` |
| OpenZero Zero for Gemma 4 E4B | 2,033 | `2f28bcc9774d12ec932eb9a55871ebef76b7b60b1ff4d52803ce6fbf86f09150` |
| Total | 4,380 | N/A |

Each source card marks its composite licence as `other`. Therefore the source rows are evidence inputs, not publication assets. This is an important distinction: a hash can support reproducibility without granting a right to redistribute the underlying bytes.

## 3. Deterministic curation

### 3.1 Schema validation

A row is accepted only if `messages` is a list with at least two non-empty string messages, all roles are present, at least one role is `user`, and the final role is `assistant`. JSON parse failures and schema failures share the `malformed` rejection class.

### 3.2 Exact-conversation identity

Messages are serialized as canonical JSON with sorted keys and compact separators. SHA-256 of this canonical representation is the row identity. This removes byte-level formatting differences from the identity calculation while retaining message content and role order. In the audited snapshot, 1,637 rows repeated an already accepted conversation.

### 3.3 Narrow credential-like screening

The curator rejects text matching a case-insensitive pattern for labels such as `api key`, `password`, `secret`, or `token`, followed by a 16-character-or-longer alphanumeric-like value. No rows in this snapshot matched. This is a narrow guard, not a complete privacy scanner: unlabelled credentials, personal data, unusual encodings, and contextual secrets can evade it.

### 3.4 Prompt-group isolation

For every accepted conversation, the final user message is hashed to form a group key. All rows sharing that key remain in the same partition. Group keys are shuffled with seed `20260809`; groups are allocated to evaluation until the requested five-percent target is met. Because groups vary in size, the exact evaluation fraction need not equal five percent.

| Curated result | Rows | Share of accepted |
|---|---:|---:|
| Accepted | 2,743 | 100.00% |
| Training | 2,606 | 95.01% |
| Evaluation | 137 | 4.99% |
| Exact duplicates rejected | 1,637 | N/A |
| Malformed rejected | 0 | N/A |
| Credential-pattern rejected | 0 | N/A |

The training file hash is `88b4927bc1b5123270e8d25be29217ebfcf9612bdf91c0e5a28e708bd1f5da6a`; the evaluation file hash is `7daa719b1c4068304d5cb3c42249e30e36f60e5edb1ab7812391a4b1ce32bd78`.

## 4. Model experiment design

### 4.1 Separate specialists

The factory defines one Qwen specialist and one Gemma specialist. Each uses its own official tokenizer and architecture. The configuration snapshot names `Qwen/Qwen3-4B` and `google/gemma-4-E4B-it`; these names are experiment inputs, not claims of endorsement. Exact immutable revisions must be pinned before a real run.

The proposed adaptation uses 4-bit NF4 loading, BF16 computation, rank-32 LoRA, alpha 64, dropout 0.05, and `all-linear` target modules. Each configuration proposes two epochs, a per-device batch size of one, gradient accumulation of 16, and a 4,096-token limit. These are initial parameters requiring measurement, not optimized values.

### 4.2 Why QLoRA

QLoRA backpropagates through a frozen 4-bit base into trainable low-rank adapters, reducing memory use relative to full-parameter tuning. The local design follows this general method but does not inherit the original paper's performance results. The QLoRA paper and current TRL documentation support the mechanism and adapter workflow, not the quality of OpenZero data or derivatives.

### 4.3 Combined student, not weight merge

Directly averaging Qwen and Gemma weights is invalid because the architectures, parameter layouts, and tokenizers differ. A combined model, if pursued, is a Qwen-based student trained on responses independently generated by evaluated specialists. The generation script writes both drafts with `review_status: pending`. A second script fails closed unless a reviewer sets `review_status: approved` and supplies `selected_answer`. No teacher-output dataset is included in this release, and no combined student is claimed.

## 5. Promotion and release gates

An experiment may advance only through the following gates:

1. freeze input hashes, base repository identifiers, immutable base revisions, dependency versions, seed, and configuration;
2. verify schema, exact duplicate counts, prompt-group non-overlap, privacy screens, and dataset rights;
3. run a finite GPU smoke test and record hardware, logs, loss, adapter hash, and failure state;
4. compare the adapter against the exact base on a disjoint held-out suite using the same prompts, decoding, scoring, and runtime;
5. check regressions in instruction following, tool selection, factual calibration, privacy, and refusal boundaries;
6. merge only a passing adapter into a high-precision base, then convert and quantize with pinned tools;
7. hash the final artifact and run real inference through the intended serving path; and
8. publish only when data, base-model, and generated-output licences permit distribution.

A failed candidate remains a documented result. It must not be repaired on the held-out suite until it passes, because repeated tuning against the gate converts evaluation data into training guidance.

## 6. Reproducibility evidence

Five Python factory modules were compiled with Python's `py_compile`: data preparation, specialist training, two-teacher generation, approved-pair conversion, and merge/export staging. The public verifier checks that the methodology manifest is internally consistent, that output counts sum correctly, and that all declared SHA-256 values have valid syntax. With the private `--curated-dir` option, it additionally recomputes split counts and hashes and rejects any final-user-prompt overlap.

Compilation verifies syntax only. It does not load model weights, allocate a GPU, prove dependency compatibility, demonstrate successful optimization, or establish behavioral improvement.

## 7. Comparison with prior methods

This work uses supervised fine-tuning and QLoRA rather than introducing a new optimizer or base architecture. Its methodological emphasis is elsewhere: prompt-group isolation for conversational variants; release gating across data, adapter, merge, conversion, and serving artifacts; and explicit separation between teacher drafts and approved distillation rows. Current TRL supports conversational SFT and PEFT adapters, while the Qwen3 report and Gemma model materials describe the respective base families. Those external sources do not validate this corpus.

## 8. Threats to validity and limitations

- Exact deduplication does not detect paraphrases, templated variants, or semantic contamination.
- Grouping only by the final user prompt may miss leakage through earlier turns, answers, source documents, or near-duplicate prompts.
- The credential expression is intentionally narrow and cannot establish privacy.
- Some source rows are synthetic or transformed; factual and coding errors may survive schema validation.
- A small local evaluation suite cannot establish broad capability, fairness, safety, or robustness.
- Loss reduction alone is not evidence of usefulness; base-versus-adapter behavioral comparison is required.
- The configuration uses evolving libraries and model repositories. Immutable revisions and lockfiles are mandatory for future execution.
- The Gemma-targeted corpus is text-only and cannot establish multimodal improvement.
- Dataset and derivative-weight redistribution remain blocked pending an explicit rights review.

## 9. Falsifiable claims

1. Given the three exact input hashes and curator version, rerunning with seed `20260809` produces 2,606 training and 137 evaluation rows.
2. No exact final-user-prompt string appears in both produced partitions.
3. The published summary hashes match the corresponding private snapshot files.
4. The approved-pair builder produces no output dataset when zero rows have both approval and a selected answer.
5. A derivative is not promoted if it fails the predeclared exact-base held-out comparison or any release gate.

Claims 1-4 are directly testable with authorized access to the private snapshot. Claim 5 is a governance rule whose evidence is the retained promotion record.

## 10. AI-use disclosure

I used OpenAI Codex to inventory files, run deterministic checks, compare implementation details with primary literature, draft and format the manuscript, and build the reproducibility package. I remain responsible for the scope, claims, code, release decision, and correction of errors. AI assistance is not independent validation or peer review.

## 11. Data, code, and licensing

The manuscript and public reproducibility metadata are released under CC BY 4.0. The verifier is released under MIT. Dataset rows, teacher outputs, private evaluations, adapter weights, and model weights are excluded. Their absence is deliberate because source rights and experimental promotion gates are unresolved.

## References

1. T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, “QLoRA: Efficient Finetuning of Quantized LLMs,” arXiv:2305.14314, 2023. https://arxiv.org/abs/2305.14314
2. A. Yang et al., “Qwen3 Technical Report,” arXiv:2505.09388, 2025. https://arxiv.org/abs/2505.09388
3. Hugging Face, “Supervised Fine-tuning Trainer,” TRL documentation. https://huggingface.co/docs/trl/main/en/sft_trainer
4. Google DeepMind, “Gemma 4 model family.” https://deepmind.google/models/gemma/gemma-4/

## Appendix A. Evidence ledger

| Evidence | Result | Boundary |
|---|---|---|
| Three input JSONL hashes | Recorded exactly | Rows not distributed |
| Curated manifest | 2,743 accepted; 2,606 train; 137 eval | Local snapshot |
| Exact duplicate rejection | 1,637 | Semantic duplicates not measured |
| Prompt overlap assertion | No exact final-prompt overlap | Earlier-turn and semantic leakage remain possible |
| Factory syntax check | 5/5 modules compiled | No training or inference implied |
| Licences | Composite datasets marked `other` | Redistribution blocked |
| Training status | Methodology only | No full specialist success claimed |
| Peer review | None | Public working paper |
