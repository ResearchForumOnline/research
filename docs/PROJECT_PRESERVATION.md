# Project preservation — 30 September 2026

Author: Shafaet Brady Hussain.

## Durable locations

| Work | Preserved location | Scope |
| --- | --- | --- |
| OpenZero runtime | https://github.com/ResearchForumOnline/OpenZero | Self-hosted code, source candidates, training workspace, independent nodes |
| OpenZero static home | https://researchforumonline.github.io/OpenZero/ | Free static documentation and release links; no inference or required node |
| ZeroThink Local engine | [Public source](https://github.com/ResearchForumOnline/ZeroThink) | New Apache-2.0 portable research engine: selected-document retrieval, nine processes, optional bounded draft/critique/revision |
| ZeroThink independent CLI | [Download v1.0.0](https://github.com/ResearchForumOnline/ZeroThink/releases/tag/v1.0.0) | Dependency-free Node.js 22+ CLI; default offline evidence map, optional operator-selected Ollama or compatible server |
| ZERO ONE desktop integration | [Published 8.0 source](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop) · [Release/submission evidence](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/blob/main/docs/qa/RELEASE_8.0.0.md) · [General Store listing](https://apps.microsoft.com/detail/9PMPR7PTW025) | Microsoft accepted the 8.0.0 update; Update in certification on 30 September 2026. Version 7.9.6 remains the verified live Store version; no claim of public 8.0 certification, Store signing or installation |
| ZERO ONE direct 8.0 downloads | [Windows x64, macOS Apple Silicon and Linux x64 release](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/releases/tag/v8.0.0) | Published direct downloads and SHA256SUMS; separate from the pending Microsoft Store update |
| ZMath implementation | https://github.com/ResearchForumOnline/ZMath | Browser encryption code, local workspace, synthetic tests and source hashes |
| ZMath static app | https://researchforumonline.github.io/ZMath/ | Public static delivery; file/message encryption runs in the browser, no accounts or API |
| ZMath dual-key vault | [Use the static app](https://researchforumonline.github.io/ZMath/dual-key/) · [Source and compatibility guide](https://github.com/ResearchForumOnline/ZMath/blob/main/dual-key/README.md) · [Download v1.1.0](https://github.com/ResearchForumOnline/ZMath/releases/tag/v1.1.0) | Browser-only encrypted notes and attachments, using separately derived passphrase and visual-pattern AES-256-GCM layers |
| Protected device-envelope research | [Preserved source guide](https://github.com/ResearchForumOnline/ZMath/blob/main/preserved/protected-mail/README.md) | Original signed-envelope research and tests, distinct from live mail delivery, identity verification or post-quantum claims |
| QuantumEncryption1 public pages | https://github.com/ResearchForumOnline/ZMath/tree/main/archive/quantumencryption1 | Static historical archive of 17 former public pages; forms and APIs removed |
| Zero Boundary Algebra | [Read preserved paper](../papers/zero-boundary-algebra-formal-specification-1.1.md) | Typed state/provenance calculus and reproducibility artifacts |
| Boundary completion and cycle memory | [Read preserved paper](../papers/zba-boundary-completion-cycle-memory-0.1.md) | Original uploaded working-paper PDF and index |
| ZME1 research | [Read preserved paper](../papers/zmath-shield-zme1-evidence-containers-1.0.md) | Dated specification, source hashes, cryptographic claims and limitations |
| Quantum evidence research | [Read preserved paper](../papers/quantum-ready-evidence-graphs.md) | Classical/synthetic evaluation, separate from hardware advantage claims |
| Formatted paper archive | [11 PDF/DOCX pairs](../papers/formatted/README.md) | Original formatted copies of existing public manuscripts with byte hashes and original rights |
| Offline public preservation kit | [Download the complete kit](https://github.com/ResearchForumOnline/research/releases/download/project-preservation-2026-09-30/public-preservation-kit-20260930.zip) · [SHA-256](https://github.com/ResearchForumOnline/research/releases/download/project-preservation-2026-09-30/public-preservation-kit-20260930.zip.sha256) | Five public source ZIPs, 612 committed files, start guide, source/license records, VERIFY.ps1 and checksums; original rights remain intact |

## Service status and interpretation

The author reports retirement of the former dynamic OpenZero, ZeroThink,
CallChat, Zmail and QuantumEncryption1 hosting. TalkToAI remains a static public
hub. A repository, archive or historic benchmark does not demonstrate that a
former service is live or that a historical marketing claim is validated.

GitHub source and release assets preserve work independently of those domains.
Users operate their own local runtimes and choose their own providers. Direct
peer exchange in OpenZero is optional; it does not establish distributed model
training, inference, consensus or a blockchain.

ZeroThink Local 1.0 is a new independent source release, distinct from the former
hosted service and its dated benchmarks. Offline operation retrieves selected
document excerpts and produces an evidence map and checklist. Optional model
operation performs at most three bounded draft, critique and revision calls to
the operator's chosen runtime. It does not perform autonomous computer takeover,
rewrite model weights, prove claims, or establish AGI. Source-ID validation checks
references to selected excerpts, not the truth or adequacy of a scientific claim.

## Verified source releases, 30 September 2026

| Release | Recorded source / asset evidence | Scope of verification |
| --- | --- | --- |
| [ZeroThink Local v1.0.0](https://github.com/ResearchForumOnline/ZeroThink/releases/tag/v1.0.0) | Source commit `473a128c13798023bb719969c286204c12df60bd`; ZIP SHA-256 `3b2421d93abb46a1e7110ac3c49395279b02fea5c5264c2810a6546cc6334b1d` | 36 focused software tests, syntax checks and standalone synthetic CLI checks; [Windows/macOS/Linux CI](https://github.com/ResearchForumOnline/ZeroThink/actions/runs/36729674345) succeeded. Downloaded release hash matched GitHub's asset digest. |
| [ZMath Local v1.1.0](https://github.com/ResearchForumOnline/ZMath/releases/tag/v1.1.0) | Source commit `1c287b3a3058273254651db16e46dca24b0ea789`; ZIP SHA-256 `aceebfb1adabbedc9eb1e7bf71e38d15d1e70338d08320eea5ccdeb78ae2ac1e` | Published release records retained regression programs, 17 added named tests, synthetic browser vault checks and historical archive/source-hash verification. This is author-controlled implementation evidence, not independent cryptographic certification. |
| [ZERO ONE 8.0 source and Store candidate](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/blob/main/docs/qa/RELEASE_8.0.0.md) | Source commit `9a433e69ef5826114250995da951b6a5427f57f1`; reviewed AppX SHA-256 `113ecb98b691c47585842d1eb5165c6685902ca810316432fdab862468d3f3b2`, 172764983 bytes | 46 Vitest and 56 Node tests passed; exact package displayed Validated and accepted as submission `1152921505702011222`. Update in certification, with automatic publication scheduled if certification passes. |

The ZERO ONE source release is available now. Microsoft certification and Store
publication remain separate pending outcomes. Version 7.9.6 is the currently
verified live Store version. The linked release record includes the Windows App
Certification Kit overall PASS and the optional Blocked executables scan FAIL;
the package is not described as passing every individual scan or as Microsoft
certified. The source and package checks do not establish a Store-signed 8.0
installation or sustained model-quality performance.

ZERO ONE direct release source commit `ab5eb1ba2b95ed5036bc78a6a699312da59bb6a9`
has successful [Windows/macOS/Linux verification, packaging and publication](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/actions/runs/36734515550)
and [source checks](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/actions/runs/36734126343).
These direct-download outcomes do not change the recorded pending Store state.

The offline public kit is 5,347,190 bytes; ZIP SHA-256 is
`80049738ef440149bd6819ef95227f770255138d71d116d413b6358b086bedc4`.
Its downloaded hash matches GitHub's published asset digest. The kit preserves
five reviewed public repository snapshots and their licenses rather than changing
or merging their rights. It is frozen at its construction time: its research
snapshot records commit `c0b8b110cc326c809d8b577da95d23bf8df39054`, before this
later index update. No kit snapshot was rewritten for this documentation change.

The ZMath visual pattern has fewer than one million possible sequences, under
20 bits before user-selection bias; a long unique passphrase provides the main
strength. Two AES-256-GCM layers do not mean AES-512. Different historical
formats are not silently converted, and original factors remain necessary for
legacy Exclusive files. Preserved signed-envelope code does not establish a
current mail service, verified human identity directory or post-quantum protocol.

## Rights and sensitive-data boundary

New ZeroThink Local code is Apache-2.0 open source, copyright 2026 Shafaet Brady
Hussain. That grant covers the reviewed new engine and its published materials;
it does not publish or relicense the old private hosted service, user data,
separately licensed ZMath code, or historical papers. Earlier paper licenses,
attribution, disclosures and source hashes remain unchanged.

Newly released author-owned ZMath code is licensed for noncommercial purposes
under PolyForm Noncommercial 1.0.0. This restriction is on the licensed code and
material, not a claim of ownership over mathematical ideas or standard AES,
PBKDF2 or HKDF algorithms. Previously released CC BY papers and permissively
licensed third-party material retain their original licenses. No credentials,
private keys, customer records, personal mail, DNA data, databases or runtime
vaults are part of this preservation release.

The ZMath code hash is recorded against the published August 2026 paper. Tests
are author-led implementation checks, not independent cryptographic auditing
or certification. The former public website pages have an explicit historical
banner and make no current offer or service commitment.
