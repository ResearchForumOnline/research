# ResearchForumOnline Research

Public research-paper releases generated from the public [Research Forum Online](https://research.talktoai.org) corpus using the ZeroThink Paper Creator method.

This repo is designed for clean, citeable public work:

- source-ledger first
- claim/evidence graph before synthesis
- careful academic wording
- no private ZMath, ZeroThink, server, or key material
- generated working papers ready for human review

## Public Workflow Links

- [TalkToAI ecosystem](https://talktoai.org/) - public project hub, course, docs, and product routes.
- [CallChat ZERO](https://callchat.org/) - Matrix-compatible secure communication and Shield licensing lane.
- [Benchmark Results](BENCHMARKS.md) - Shafire, Spectra, TalkToAI, and OpenZero public benchmark snapshots.
- [QuantumEncryption1 Paper Creator evidence workflow](https://quantumencryption1.com/paper-creator-evidence-workflow/) - student and research workflow for survey expansion, source ledgers, and claim/evidence/provenance graphs.
- [Quantum-ready evidence workflow](https://quantumencryption1.com/quantum-evidence-workflow/) - controlled PoC lane for provenance graphs and classical versus simulator/quantum optimisation tests.
- [ZeroThink Paper Creator](https://zerothink.talktoai.org/research-paper-creator) - live research-paper drafting tool.

## New Working Papers

| Paper | Focus |
| --- | --- |
| [Zero Boundary Algebra 1.1: Formal Specification](papers/zero-boundary-algebra-formal-specification-1.1.md) | Expanded typed algebra, executable verifier, property results, encryption-profile audit, privacy/governance analysis, and falsifiable evaluation protocol |
| [Zero Boundary Algebra 1.0: Formal Specification](papers/zero-boundary-algebra-formal-specification-1.0.md) | Preserved first formal release |
| [ZeroThink 1.0: A Reproducible Architecture for Evidence-Gated AI Agent Services](papers/zerothink-reproducible-architecture-1.0.md) | Consolidated architecture, dated positive and negative evidence, executable release-invariant tests, and falsifiable baselines |
| [ZMath Shield and ZME1 1.0: Authenticated Evidence Containers](papers/zmath-shield-zme1-evidence-containers-1.0.md) | Standard-primitive envelope specification, frozen source hashes, regression evidence, threat model, and structural negative vectors |
| [Zmail and CallChat 1.0: Layered Protected Communications](papers/zmail-callchat-protected-communications-1.0.md) | Evidence-bounded email, Matrix messaging, object, device, and call-media protection with explicit downgrade rules |
| [OpenZero 1.0: A Local-First Agent Runtime](papers/openzero-local-first-agent-runtime-1.0.md) | Frozen runtime architecture, serving-path failures, offline boundaries, and explicit tool-authority risks |
| [OpenZero Model and Dataset Methodology 1.0](papers/openzero-model-dataset-methodology-1.0.md) | Deterministic private-corpus curation, prompt-group isolation, QLoRA experiment gates, and rights-bounded release controls |
| [ZeroMint AIOS Engineering Evaluation 1.0](papers/zeromint-aios-engineering-evaluation-1.0.md) | Live distribution metadata, split-image and torrent integrity checks, installer boundaries, and supply-chain gaps |
| [Cymatics Zero Platform Evaluation 1.0](papers/cymatics-zero-platform-evaluation-1.0.md) | Synthetic-corpus and browser-audio audit, live count inconsistency, and generator reproducibility failure |
| [Quantum-Ready Evidence Graphs and QPU-Factor Evaluation 1.0](papers/quantum-ready-evidence-graphs.md) | Exact classical claim-graph baseline, greedy comparison, and synthetic-fixture QPU-factor contract boundary |
| [Probability of Goodness Decision Routing 1.0](papers/probability-of-goodness-ethical-routing.md) | Frozen substring-score audit, eight synthetic counterexamples, and hard-rule-first routing specification |
| [Bio-Inspired Recursive Computation 1.0](papers/bio-digital-research-boundaries.md) | Frozen genetic-formula audit, bounded recurrence, and explicit metaphor-to-biology evidence boundaries |
| [Zero Boundary Algebra as a Provenance Workflow](papers/zero-boundary-algebra-provenance-workflow.md) | Public mathematical/workflow framing |
| [ZeroThink as a Sovereign Reasoning Layer](papers/zerothink-sovereign-reasoning-layer.md) | Research writing and audit workflow |
| [OpenZero and Local-First AI Nodes](papers/openzero-local-first-ai-nodes.md) | CPU-friendly sovereign agents |
| [ZMath Shield and Portable Evidence Containers](papers/zmath-shield-evidence-containers.md) | Public behaviour spec, no private encryption code |
| [Shafire and OpenZero Local Benchmark Snapshot](papers/shafire-openzero-local-benchmark-2026-07-08.md) | First CPU/API benchmark snapshot for Shafire models and OpenZero |
| [Spectra8, TalkToAiQ, and SpectraMind OpenZero Benchmark](papers/spectra-talktoaiq-openzero-benchmark-2026-07-08.md) | Requested benchmark pass for Spectra/TalkToAiQ/SpectraMind artifacts |
| [Separating Model Artifact Performance from Serving-Path Failure](papers/local-llm-serving-path-benchmark-2026-07-26.md) | Methods-and-results preprint on local-route template contamination and reproducible exact-answer testing |
| [ZeroThink Public System Benchmark](papers/zerothink-system-benchmark-2026-07-09.md) | Public live-route, API-guard, CLI-device-flow, and OpenZero integration benchmark |
| [Boundary-Oriented Evaluation of a Deployed AI Agent Service](papers/zerothink-public-boundary-evaluation-2026-07-26.md) | Methods-and-results preprint built from the reproducible public-surface benchmark; includes limits and conflict disclosure |
| [ZeroThink Authenticated Intelligence Benchmark](papers/zerothink-authenticated-intelligence-benchmark-2026-07-09.md) | Account-routed exact-answer comparison across ZeroThink/OpenZero and saved provider lanes |
| [Botanical Formula Research Roadmap](papers/botanical-formula-research-roadmap.md) | Safety-first research plan |
| [Research Forum Corpus Synthesis 2026](papers/research-forum-corpus-synthesis-2026.md) | Umbrella map of the corpus |

## Source Ledger

- [Research Forum Source Ledger](sources/research-forum-source-ledger.md)
- [Machine-readable source index](data/research-forum-source-index.json)

## How The Papers Were Built

The generator crawls public forum pages, indexes first-post text, filters likely spam/noise, marks third-party posts separately, then applies the public ZeroThink Paper Creator protocol.

Run:

```bash
python tools/build_research_release.py
```

## Safety Boundary

Read [PUBLIC_RELEASE_BOUNDARY.md](PUBLIC_RELEASE_BOUNDARY.md) before adding material. This repo is public research text only. It does not publish proprietary encryption code, private prompts, keys, credentials, customer data, or live-server internals.
