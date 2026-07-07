# ResearchForumOnline Research

Public research-paper releases generated from the public [Research Forum Online](https://research.talktoai.org) corpus using the ZeroThink Paper Creator method.

This repo is designed for clean, citeable public work:

- source-ledger first
- claim/evidence graph before synthesis
- careful academic wording
- no private ZMath, ZeroThink, server, or key material
- generated working papers ready for human review

## New Working Papers

| Paper | Focus |
| --- | --- |
| [Zero Boundary Algebra as a Provenance Workflow](papers/zero-boundary-algebra-provenance-workflow.md) | Public mathematical/workflow framing |
| [ZeroThink as a Sovereign Reasoning Layer](papers/zerothink-sovereign-reasoning-layer.md) | Research writing and audit workflow |
| [OpenZero and Local-First AI Nodes](papers/openzero-local-first-ai-nodes.md) | CPU-friendly sovereign agents |
| [ZMath Shield and Portable Evidence Containers](papers/zmath-shield-evidence-containers.md) | Public behaviour spec, no private encryption code |
| [Quantum-Ready Evidence Graphs](papers/quantum-ready-evidence-graphs.md) | AI claim graphs plus constrained optimisation tests |
| [Probability of Goodness](papers/probability-of-goodness-ethical-routing.md) | Ethical routing heuristic |
| [Bio-Digital Research Boundaries](papers/bio-digital-research-boundaries.md) | DNA/organic computing caution lane |
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
