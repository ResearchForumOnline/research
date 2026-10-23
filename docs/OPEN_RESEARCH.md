# Research, original source and reuse rights

Catalog reviewed 23 October 2026. Author: Shafaet Brady Hussain.

The [research index](../README.md) links the public manuscripts, source ledgers,
formatted originals and reproducibility code. The machine-readable
[public research catalog](PUBLIC_RESEARCH_CATALOG.json) inventories the exact
Git-tracked research files and their SHA-256 hashes. A public paper, a reference
implementation and a complete application are different research outputs.

## Find the work

| Research output | Public location | Scope |
| --- | --- | --- |
| Zero Boundary Algebra 1.1 | [Manuscript](../papers/zero-boundary-algebra-formal-specification-1.1.md) and [reference artifacts](../artifacts/zba-1.1/) | Typed state calculus, executable reference and published evaluation |
| Boundary completion and cycle memory | [Original paper index](../papers/zba-boundary-completion-cycle-memory-0.1.md) | Preserved supplied PDF, working draft and its disclosures |
| Reset compatibility | [Paper and proofs](../papers/zba-reset-compatibility-0.1.md) and [reproducibility package](../artifacts/zba-reset-compatibility-0.1/) | Transformation monoids, exhaustive small cases and validator synthesis |
| Historical ZeroThink architecture | [Original architecture paper](../papers/zerothink-reproducible-architecture-1.0.md), [reference artifacts](../artifacts/zerothink-architecture-1.0/) and [formatted originals](../papers/formatted/) | Dated service architecture and evaluation evidence; these documents do not contain the full original hosted application |
| Original ZeroThink DNA Lab and full application | [Published full PHP source](https://github.com/ResearchForumOnline/ZeroThink/tree/main/web), [setup](https://github.com/ResearchForumOnline/ZeroThink/blob/main/web/README.md) and [exact restoration commit](https://github.com/ResearchForumOnline/ZeroThink/commit/7e5f8bf07e6e57286d3bac35a83fd92e90c48add) | Original DNA Lab v1.7.1 plus restored research/account-backed web source. The local DNA interface runs without MySQL or hosted login. Reference/model packs install separately; source and synthetic software checks are not biological validation |
| ZeroThink Local companion | [Companion source and CLI](https://github.com/ResearchForumOnline/ZeroThink) | The September portable engine is a separate companion and is not the full original DNA Lab |
| Bio-inspired computation | [Paper](../papers/bio-digital-research-boundaries.md) and [code](../artifacts/bio-inspired-recursive-computation-1.0/) | Deterministic formula audit and bounded recurrence, with biological-claim limits |
| Probability of Goodness | [Paper](../papers/probability-of-goodness-ethical-routing.md) and [code](../artifacts/probability-goodness-routing-1.0/) | Routing audit, synthetic counterexamples and reference contract |
| Quantum evidence graphs | [Paper](../papers/quantum-ready-evidence-graphs.md) and [code](../artifacts/quantum-evidence-qpu-factor-1.0/) | Classical/synthetic baseline and QPU-factor interface contract; no grant-funded hardware results are introduced by this catalog |
| Offline circuit protocol | [ORP-001 source, fixtures and reproduction](../artifacts/offline-circuit-protocol-1.0/) | Newly frozen four-qubit, ten-circuit local-only protocol extracted from author-owned offline helpers; 17 software tests, no service results or external execution |
| Research-corpus methods | [Paper](../papers/research-forum-corpus-synthesis-2026.md) and [code](../artifacts/research-corpus-claim-risk-1.0/) | Text-free metadata, title-based review queues and synthetic rule checks |
| OpenZero methods and independent nodes | [Runtime paper](../papers/openzero-local-first-agent-runtime-1.0.md), [model methodology](../papers/openzero-model-dataset-methodology-1.0.md), [application source](https://github.com/ResearchForumOnline/OpenZero) and [7.3.1 download](https://github.com/ResearchForumOnline/OpenZero/releases/tag/v7.3.1) | Papers, frozen reference artifacts and the separately licensed application; 7.3.1 serves its required browser client locally and fixes explicit model routing and automatic-repair controls |
| ZMath and protected communications | [ZME1 paper](../papers/zmath-shield-zme1-evidence-containers-1.0.md), [communications paper](../papers/zmail-callchat-protected-communications-1.0.md) and [application source](https://github.com/ResearchForumOnline/ZMath) | Standard-primitive protocols, reference evidence and the separately licensed browser application |
| Engineering evaluation | [Cymatics](../papers/cymatics-zero-platform-evaluation-1.0.md), [ZeroMint](../papers/zeromint-aios-engineering-evaluation-1.0.md) and [TalkToAi Code systems papers](../sources/talktoai-code-8-evidence-ledger.md) | Source-grounded engineering preprints and their stated limitations |

## Reuse the correct material under the correct terms

The [current research license grant](../LICENSE.md), effective 23 October 2026,
licenses Shafaet Brady Hussain's original, author-owned manuscripts under CC BY
4.0 and his original reference code and maintenance tools under MIT. This
includes the author's original ZeroThink architecture manuscript and formatted
copies. It does not relicense other authors' work, upstream source or datasets.

Individual papers also state earlier terms in their headers. Several papers
explicitly grant CC BY 4.0 and identify MIT reference artifacts. MIT notices exist
in the bio-inspired, Probability of Goodness, quantum-evidence and research-corpus
artifact directories. Keep the original attribution, disclosures and notices.
The formatted-paper [source manifest](../papers/formatted/SOURCE_MANIFEST.json)
records the rights found at preservation time; the archive record predates the
new grant and remains unchanged. For material outside the new grant's scope, an
absent license statement is not an open-source grant.

The separate ZMath application's published terms are PolyForm Noncommercial
1.0.0. OpenZero's published Community Source License includes commercial and
managed-service restrictions. Those are source-available application releases;
they should not be described as unrestricted open-source licenses. They do not
remove the CC BY or MIT grants already attached to individual research outputs.
Third-party source snapshots retain their original licenses.

## Check a downloaded Git checkout

Use Python 3.10 or later and Git. No account, API key, model, database, external
Python package or network connection is needed:

```console
python tools/audit_public_research.py
python tools/build_preservation_release.py
```

The first command checks this catalog against the tracked research files and
checks all 22 formatted originals against their preservation manifest. The
second builds the existing, explicit formatted-paper archive. A failed check
returns a nonzero status. After an intentional reviewed research change, update
the catalog with `python tools/audit_public_research.py --write` and commit it
with the changed research files. Files must be Git-tracked to enter the catalog.
Untracked desktop files and private source folders are never crawled.

Hashes establish correspondence with the recorded bytes. They do not establish
scientific correctness, novelty, clinical utility, external review, institutional
endorsement, ownership or a cryptographic signature. Reproducibility checks have
the particular scope stated by their papers and artifact READMEs.

## Publication scope

The original DNA lab source restoration is published in the linked application
repository. The September Local CLI remains a separate companion. This catalog
does not assert that every private research folder has been published. Personal genotype
files, customer records, production databases, private correspondence, login and
recovery material, deployment secrets and material subject to separate rights or
publication agreements are outside this repository's publication scope. Public
reference fixtures must be synthetic or have an explicit distributable source.

The [September preservation kit](PROJECT_PRESERVATION.md) remains a dated
snapshot. Its preserved files and earlier evidence have not been rewritten to
claim newer application functionality.
