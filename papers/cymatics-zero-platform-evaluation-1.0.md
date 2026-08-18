---
title: "Cymatics Zero Platform Evaluation 1.0"
author: "Shafaet Brady Hussain"
date: "2026-08-18"
license: "CC BY 4.0"
---

# Cymatics Zero Platform Evaluation 1.0
## Synthetic Pattern Corpus, Browser Audio, Research-Agent Boundaries, and Reproducibility Audit

**Shafaet Brady Hussain**

Independent researcher and developer, United Kingdom

18 August 2026

## Abstract

I evaluate Cymatics Zero as a browser-based research and creative platform rather than as a physical cymatics simulator or medical system. The inspected corpus contains 3,000 unique synthetic SVG records, evenly divided across five named visual families. Every referenced SVG exists and parses as XML; all records carry an explicit “research/art/education only” medical-claim boundary. The browser code implements three-oscillator tone playback, offline mono WAV rendering, local pattern retrieval, and bring-your-own-key model calls. The live site and pattern manifest returned HTTP 200. However, the live HTML description advertises 4,111 patterns while the served manifest contains 3,000, and the checked-in generator did not reproduce any of 25 sampled published SVGs. The published manifest also uses family names and metadata not emitted by the current script. Dependencies are unpinned as `latest`, and no lockfile or automated browser/audio test evidence was present. The visual equations are design approximations, not calibrated plate, membrane, or fluid solvers. Browser gain values do not determine acoustic sound-pressure level at a listener. No healing, biological, therapeutic, or experimentally validated resonance effect is claimed. I classify the platform as a functional synthetic-media prototype with good explicit claim boundaries, a coherent corpus snapshot, and material reproducibility, safety-measurement, dependency, and documentation gaps.

## 1. Scope and research question

The question is: which parts of Cymatics Zero are executable and testable, and which are aesthetic or aspirational? The evaluation covers the synthetic corpus, generator, browser audio implementation, AI request boundary, public site, documentation, and non-hardware tests. It excludes private API keys, live paid calls, microphone capture, physical plates, liquids, speakers, human participants, and clinical interpretation.

Cymatics is grounded here in visible or representable vibration patterns. Real Chladni figures depend on plate geometry, material, thickness, support, excitation, damping, and eigenmodes. Faraday waves depend on fluid properties, vessel geometry, forcing, and instability thresholds. A frequency label alone does not determine either pattern.

## 2. Platform architecture

The inspected platform has four client-side layers:

1. a static 3,000-record SVG pattern corpus and JSON manifest;
2. browser `AudioContext` playback and `OfflineAudioContext` WAV rendering;
3. local browser storage for provider selection, keys, and research notes; and
4. direct or proxied bring-your-own-key requests to model APIs.

An optional Node proxy is documented for cross-origin and routing control. The public architecture intentionally excludes accounts and a central user database. This reduces retained server-side personal data, but localStorage keys remain accessible to scripts executing in the same origin and should not be treated as high-security key custody.

## 3. Synthetic corpus audit

The manifest declares 3,000 unique records, with 600 records in each family.

| Family | Records | Interpretation boundary |
|---|---:|---|
| `chladni_square` | 600 | Nodal-line-inspired geometry |
| `faraday_interference` | 600 | Plane-wave interference contours |
| `radial_bessel_inspired` | 600 | Radial-mode-inspired design |
| `lissajous_rotor` | 600 | Parametric curve composition |
| `zero_metatron_lattice` | 600 | Project-specific geometric overlay |

All 3,000 referenced files exist and parse as XML. Manifest frequencies range from 108.057 to 1,113.999 Hz and normalized amplitudes from 0.15 to 0.95. These fields are design parameters. They are not measurements of resonant frequency, acoustic output, or visual fidelity to an apparatus.

The manifest SHA-256 is `c78cd76f2da991d6964ce84766c3a266cb46d4a6e559175c421988c721d57620`. The generation script SHA-256 is `05230a8b36a63d764654424fa2b3825095521f41aceaab22d8eefc1f2fbb6aff`.

## 4. Reproducibility failure

I compiled the Python generator and ran it into a separate temporary directory for 25 records. None of the 25 regenerated SVG byte hashes matched the corresponding published SVG. The mismatch is structural, not merely a timestamp: published SVGs contain different definitions and the published manifest uses family labels and metadata that the current script does not emit. Both retained research-pack copies contain the same current generator hash.

This negative result means the corpus snapshot is internally inspectable but not reproducible from the distributed generator. It does not imply that the files are corrupt. It means the build provenance is incomplete or the generator changed after corpus production.

| Reproduction check | Result |
|---|---:|
| Published records sampled | 25 |
| Byte-identical regenerations | 0 |
| Mismatches | 25 |
| Current generator syntax | Pass |

The corrective gate is to recover or identify the exact original generator, pin its dependencies and parameters, regenerate into a clean directory, and publish a manifest linking generator revision to every output hash.

## 5. Browser audio evaluation

The audio module passed JavaScript syntax checking. Playback constructs a fundamental plus 1.5x and 2x oscillators, applies per-oscillator gains, and ramps a master gain up and down. WAV export uses a mono 44.1 kHz offline context by default and serializes 16-bit PCM with a conventional RIFF/WAVE header.

The W3C Web Audio API supports both real-time `AudioContext` graphs and offline rendering. That establishes the API mechanism, not the acoustic result. Output gain is dimensionless and passes through unknown browser, operating-system, amplifier, loudspeaker, headphone, room, and distance characteristics. Therefore the software cannot infer dBA exposure or hearing safety from its gain constants.

The National Institute on Deafness and Other Communication Disorders warns that risk depends on level and duration; repeated exposure at or above approximately 85 dBA can cause hearing loss. Cymatics Zero should default to muted playback, require a user gesture, display level/duration warnings, cap duration, and encourage external sound-level measurement for physical experiments.

## 6. AI and privacy boundary

The AI module passed JavaScript syntax checking. Its system instructions explicitly reject medical and healing claims, frame frequency presets as cultural or creative parameters, and ask for testable protocols and uncertainty. Direct browser calls send the visitor's key to the selected provider endpoint. The live bundle contains localStorage logic and OpenAI/Groq provider routes.

These controls are useful but incomplete:

- prompt text cannot guarantee model behavior;
- storing a key in localStorage increases exposure to cross-site scripting or same-origin script compromise;
- a proxy must enforce strict origin checks, body limits, redacted logs, rate limits, and abuse controls;
- a live model call was not made in this evaluation; and
- generated research summaries require source verification.

## 7. Live-site consistency

On 18 August 2026, the live root page and manifest returned HTTP 200. The manifest served 3,000 records from `czp_0001` through `czp_3000`. The live HTML meta description nevertheless stated “4,111 synthetic SVG patterns.” The bundle contains fallback labels for “4,111,” “3,000 base,” and “1,111 advanced,” but the served manifest exposes only 3,000 records. The user-visible runtime count appears to prefer the loaded manifest, while search and social metadata remain overstated.

This is a falsifiable documentation defect. The public description should state 3,000 unless an additional 1,111-record manifest is actually served and its licence, hashes, and selection logic are documented.

## 8. Comparison with physical cymatics

Experimental Chladni work measures nodal patterns and resonant wave numbers on driven plates. Faraday-wave research studies parametrically forced fluid surfaces and symmetry transitions. Cymatics Zero instead generates contour art from simplified analytic expressions and geometric overlays. This makes it useful for education, generative design, interface prototyping, and experiment planning, but not a predictive finite-element or fluid-dynamics model.

The strongest scientific extension would couple each synthetic family to an explicit forward model and calibration dataset: apparatus dimensions, material constants, boundary conditions, drive acceleration, measured frequency response, camera geometry, and quantitative image similarity. Without these, the frequency-to-image mapping is decorative metadata.

## 9. Engineering scorecard

| Control | Result | Boundary |
|---|---|---|
| Manifest identity and count | Pass | 3,000-record snapshot |
| Unique IDs | Pass | Exact IDs only |
| SVG existence/XML parsing | 3,000/3,000 pass | No visual or physical validation |
| Family balance | 600 each | Curated design balance |
| Medical-claim field | 3,000/3,000 bounded | Metadata does not enforce all outputs |
| Python/JS syntax | Pass | Not runtime behavior |
| Sample regeneration | 0/25 match | Release provenance fails |
| Live manifest | 3,000 records | HTTP availability snapshot |
| Live marketing count | 4,111 | Inconsistent with manifest |
| Dependency pinning | `latest`; no lockfile | Non-reproducible build environment |
| Browser build/test | Not run | Dependencies absent; no install performed |
| Physical experiment | Not run | No resonance validation |
| Clinical evaluation | Not applicable/not run | No therapeutic claim permitted |

## 10. Release gates

1. recover the exact corpus generator and make 3,000/3,000 output hashes reproducible;
2. commit a lockfile and pin runtime/tool versions;
3. reconcile the 3,000 versus 4,111 public count;
4. add automated manifest, SVG, search, selection, WAV-header, peak-sample, and key-storage tests;
5. add browser integration tests with model calls mocked by default;
6. publish a Content Security Policy and minimize third-party same-origin scripts;
7. add calibrated SPL guidance rather than implying code-level gain is hearing-safe; and
8. keep physical and health claims behind preregistered measurements and appropriate review.

## 11. Falsifiable claims

1. The evaluated manifest contains exactly 3,000 unique records and five families of 600.
2. Every referenced SVG exists and parses as XML.
3. The current generator does not byte-reproduce the 25 sampled published SVGs.
4. The live manifest returns 3,000 records while the root meta description states 4,111.
5. The audio and AI modules pass JavaScript syntax checks.
6. No claim in this paper establishes healing, treatment, biological change, or accurate physical simulation.

## 12. AI-use disclosure

I used OpenAI Codex to inspect the corpus and code, run syntax and XML checks, regenerate a bounded sample, inspect the live public site, compare the implementation with primary technical and health sources, draft the manuscript, and build the publication package. I remain responsible for its claims and corrections. AI assistance is not peer review or independent validation.

## 13. Licensing and availability

The manuscript and public evidence summary are CC BY 4.0; the verifier is MIT. The source corpus labels its synthetic SVGs CC0-1.0. This paper does not relicense third-party libraries, model services, trademarks, or external research.

## References

1. T. D. Rossing, “Exploring the resonant vibration of thin plates: Reconstruction of Chladni patterns and determination of resonant wave numbers,” Journal of the Acoustical Society of America, 2015. https://doi.org/10.1121/1.4916704
2. W. S. Edwards and S. Fauve, “Patterns and quasi-patterns in the Faraday experiment,” Journal of Fluid Mechanics, 1994. https://doi.org/10.1017/S0022112094002030
3. W3C, “Web Audio API.” https://www.w3.org/TR/webaudio-1.0/
4. NIDCD, “Noise-Induced Hearing Loss.” https://www.nidcd.nih.gov/health/noise-induced-hearing-loss
5. Cymatics Zero live platform. https://cymatics.talktoai.org/

## Appendix A. Evidence ledger

| Evidence | SHA-256 or result | Limitation |
|---|---|---|
| Pattern manifest | `c78cd76f2da991d6964ce84766c3a266cb46d4a6e559175c421988c721d57620` | Snapshot only |
| Generator | `05230a8b36a63d764654424fa2b3825095521f41aceaab22d8eefc1f2fbb6aff` | Does not reproduce sample |
| Audio module | `bdaca3fc84bf63f35ac1609343c8574cedf5007770c5d3ad2c93ea4495aef27e` | Syntax only |
| AI module | `91db58def85dc71fffa651daafaafb4ccf47effea9390cbb9e358217f8191d6c` | No paid call made |
| Live bundle | `cbe17ce571becc5bbedd0b70afef50c17c98f59de3aa728de3aa766a25008ae2` | Retrieved 2026-08-18 |
| SVG audit | 3,000/3,000 pass | XML validity, not physics |
| Reproduction sample | 0/25 match | Negative result |
| Peer review | None | Public working paper |
