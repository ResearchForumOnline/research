---
title: "Research-Corpus Curation and Claim-Risk Benchmark 1.0"
author: "Shafaet Brady Hussain"
date: 2026-08-18
status: "independent technical working paper"
license: "CC BY 4.0 paper; MIT reproducibility code"
---

# Research-Corpus Curation and Claim-Risk Benchmark 1.0

## A Text-Free Metadata Audit and Review-Queue Baseline for ResearchForumOnline

Shafaet Brady Hussain | Independent researcher, ResearchForumOnline | 18 August 2026

## Abstract

I consolidate the Research Forum Online corpus synthesis into a reproducible curation and triage study. The frozen public index contains 134 records: 123 classified by the existing generator as primary-author corpus items, five as third-party forum sources, and six as likely-spam exclusions. A text-free metadata snapshot preserves identifiers, titles, URLs, hashes, word counts, and provenance lanes without redistributing post bodies or excerpts. Structural checks find zero missing required records, duplicate URL groups, duplicate text-hash groups, nonpositive word counts, or replacement-character titles in that snapshot. A transparent title-keyword baseline queues 50 records across medical, genetic/biological, quantum, and extraordinary-claim categories; no security title matched the current vocabulary. A 12-case synthetic rule self-test achieves 1.0 micro-precision and recall by construction and tests implementation mechanics only. It is not empirical validation on real claims. The benchmark does not determine truth, quality, danger, misconduct, author intent, or scientific validity.

## 1. Research question and contribution

How can a heterogeneous author corpus be curated into reviewable research lanes while preserving provenance and avoiding automatic judgments about truth? The earlier umbrella synthesis mapped themes but offered no executable corpus-quality or triage benchmark. This version replaces that broad draft with a frozen metadata artifact, deterministic checks, explicit rule vocabulary, measured queue counts, and release gates.

The intended unit is a review queue, not a verdict. A record may be queued because its title contains a high-stakes or extraordinary topic even when the post itself is cautious, corrective, historical, or explicitly sceptical. Conversely, a consequential claim may evade the queue if its title uses unlisted language.

## 2. Frozen corpus and provenance lanes

The source index was generated on 7 July 2026 from public first posts on `research.talktoai.org`. The crawler records topic metadata, first-post text hashes, word counts, excerpts, and full text. Its author classifier treats starters named support, admin, shafaet, shaf, or zero as author-controlled. It marks five other starters as third party and applies a small spam-term list before choosing a publication lane.

Those rules are operational conventions, not identity proof. Account labels can be incomplete or compromised, and “primary-author corpus” means selected by this generator—not independently authenticated authorship. Likely spam is similarly a heuristic label.

The release exports only metadata needed for reproducibility. It excludes first-post text and excerpts, limiting redistribution of third-party copyrighted material and reducing accidental disclosure while retaining hashes for correspondence checks.

## 3. Structural data-quality audit

The verifier checks six required fields: ID, title, URL, text SHA-256, word count, and publication lane. It counts missing records, duplicate URL groups, duplicate content-hash groups, nonpositive word counts, and titles containing the Unicode replacement character.

Across 134 frozen records, all five defect counts are zero. This supports only structural completeness and exact-duplicate absence within the snapshot. It does not detect paraphrase duplication, near-duplicate drafts, incorrect extraction, truncated pages, stale URLs, false authorship, hallucinated citations inside posts, or semantic contradictions.

Dataset documentation should describe motivation, composition, collection, preprocessing, uses, distribution, and maintenance rather than presenting a file as self-explanatory [1]. The FAIR principles similarly distinguish findability, accessibility, interoperability, and reusability [2]. This package advances provenance and reproducibility but does not satisfy every documentation or long-term maintenance requirement.

## 4. Claim-risk triage baseline

The title-only classifier uses five disclosed keyword sets: medical; genetic/biological; security; quantum; and extraordinary. Any match places the record in a category. The categories deliberately overlap.

Fifty of 134 titles match at least one category. Counts are: 16 extraordinary, 16 genetic/biological, 13 medical, 12 quantum, and zero security. Overlap explains why category totals exceed the unique flagged count. Zero security matches is a diagnostic result, not evidence that security claims are absent; the vocabulary and title-only boundary are too narrow.

The queue should prioritize evidence review according to consequence: health and biological-effect wording needs domain expertise; encryption and security assurance needs threat models and standard-primitive evidence; quantum wording needs simulator/hardware separation; extraordinary claims need especially clear hypothesis and evidence labels. A match does not imply the claim is false or irresponsible.

## 5. Synthetic rule self-test

Twelve synthetic titles exercise empty, single-label, and multilabel cases. Against labels authored from the same published vocabulary, the implementation returns 12 true-positive labels, zero false positives, and zero false negatives: micro-precision 1.0 and micro-recall 1.0.

This perfect result is intentionally not described as model performance. It confirms that the code implements its own rule specification. Because test labels are constructed from that vocabulary, the result contains no independent annotation, real-world ambiguity, prevalence estimate, or generalization evidence. Future empirical benchmarking requires a separately labelled sample, blinded annotation, disagreement reporting, and locked evaluation data.

## 6. Curation workflow

An evidence-bounded publication workflow should proceed in stages:

1. Freeze the source snapshot and hash the generator, index, and ledger.
2. Separate author-controlled, third-party, and excluded lanes before synthesis.
3. Preserve source IDs and hashes through every derived paper.
4. Run structural checks and near-duplicate review.
5. Create consequence-sensitive review queues without treating them as truth labels.
6. For each paper, record claim, source, evidence type, external comparison, limitation, falsifier, and release decision.
7. Require human review for medical, biological, security, identity, legal, or other consequential claims.
8. Publish immutable packages and verify live asset hashes.

The eleven preceding publication-program papers demonstrate this consolidation pattern: broad concept notes were replaced by narrower formal specifications, negative results, frozen-source audits, and reproducibility packages rather than being released as overlapping promotional drafts.

## 7. Threats to validity and misuse

Title keywords miss euphemisms and contextual meaning, trigger on negation and critique, and reflect English vocabulary. Counts depend on one historical snapshot. The generator’s support-author list and spam terms are not authentication or robust moderation. Exact hashes find exact duplicates only. Public views and dates are not quality signals. A future user could misuse risk categories to stigmatize authors or suppress unconventional research.

Accordingly, the benchmark must not rank people, infer intent, automate removal, make clinical or legal judgments, or substitute for peer review. Reviewers should see the matched term, source lane, and full context; they should be able to clear, relabel, or escalate a record with reasons.

## 8. Falsifiable claims and release gates

1. The included snapshot must contain 134 records with lane counts 123, five, and six.
2. The structural defect counts must reproduce from the frozen metadata.
3. The 12 synthetic cases must reproduce their declared rule labels.
4. Any vocabulary change requires a new version and rerun; prior counts must not be silently overwritten.
5. Real-world precision or recall must not be claimed without independent labels from a held-out sample.
6. Source-text redistribution requires a separate rights review; the public benchmark remains metadata-only.
7. A corpus refresh must record retrieval time, failures, changed hashes, additions, removals, and generator revision.

## 9. Limitations

The benchmark uses one July 2026 crawl and was not refreshed live for this release. It evaluates titles, not full claims. The synthetic suite is specification testing, not independent ground truth. There is no inter-annotator study, near-duplicate model, citation verifier, plagiarism analysis, demographic audit, peer review, or independent validation. Counts describe the frozen public index and may not describe the current website.

## 10. Conclusion

The corpus can be made more publishable by treating curation as an evidence system: freeze provenance, minimize redistributed text, measure structural defects, route consequential topics for review, and distinguish rule self-tests from empirical accuracy. The released benchmark is intentionally simple enough to inspect and falsify. Its most important result is the boundary it enforces: a review signal is not a judgment of truth or worth.

## Evidence ledger

- Source index: `data/research-forum-source-index.json`, SHA-256 `953d8e915d0fed54306f4e22ddebc3097d73900778f9850bd4d21ab9fb5ad71a`.
- Generator: `tools/build_research_release.py`, SHA-256 `e115e55941c6e8f5e75a0e4664c1cf0caa35c91b12f89e9cd33af5f424142040`.
- Source ledger: `sources/research-forum-source-ledger.md`, SHA-256 `54732ea0748310d1d880d9c2fb8abf9be9a2cbd165a4c77efd583e229b153b06`.
- Reproducibility package: `artifacts/research-corpus-claim-risk-1.0/`.

## AI-use disclosure

AI tools assisted corpus inspection, rule design, code generation, analysis, drafting, editing, and packaging. I take responsibility for the claims and release decisions. AI assistance is not peer review or independent validation.

## Licensing

The paper is CC BY 4.0. New benchmark code is MIT licensed. Source-site text is not redistributed in the reproducibility snapshot; titles and metadata remain subject to applicable rights and platform terms.

## References

[1] T. Gebru et al. “Datasheets for Datasets.” *Communications of the ACM* 64(12), 86-92, 2021. https://doi.org/10.1145/3458723

[2] M. D. Wilkinson et al. “The FAIR Guiding Principles for scientific data management and stewardship.” *Scientific Data* 3, 160018, 2016. https://doi.org/10.1038/sdata.2016.18
