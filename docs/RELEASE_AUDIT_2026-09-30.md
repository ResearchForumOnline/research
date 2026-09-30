# Published release audit — 30 September 2026

This engineering record distinguishes published Store packages, GitHub downloads,
source repairs and installed state. Version checks used current Partner Center
product overviews and live package records, public GitHub release assets and CI.
Private account screenshots, credentials and local machine configuration are not
included in this repository.

## Confirmed Store publication

| Product | Application version | Store package | Public Store listing | Matching GitHub release |
| --- | --- | --- | --- | --- |
| TalkToAi Code | 8.5.0 | 1.4.0.0 | [Microsoft Store](https://apps.microsoft.com/detail/9PPGFB30SHD9) | [Windows 8.5.0](https://github.com/ResearchForumOnline/TalkToAi-Code/releases/tag/v8.5.0) |
| ZERO ONE Desktop | 8.0.0 | 8.0.0.0 | [Microsoft Store](https://apps.microsoft.com/detail/9PMPR7PTW025) | [8.0.0 desktop downloads](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/releases/tag/v8.0.0) |
| ZSEC Browser | 0.3.28 | 0.3.28.0 | [Microsoft Store](https://apps.microsoft.com/detail/9PHBSSG3N99V) | [0.3.28 Browser and Shields](https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.3.28-browser) |
| ZSEC Antivirus | 0.3.32 | 0.3.32.0 | [Microsoft Store](https://apps.microsoft.com/detail/9N1HTFN88B1K) | [0.3.32 Windows community download](https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.3.32-windows) |

Partner Center confirmed that each latest product was available in Microsoft
Store. TalkToAi Code had passed certification and was on a manual publication
hold; the publisher completed Publish now under the owner's authorization, then
verified public availability. This does not verify an installed upgrade on the
owner's PC. Store updates and direct downloads have separate channels.

### Later Antivirus compatibility update

After that four-product publication check, a separately versioned Antivirus
0.3.33 compatibility patch was released on GitHub and submitted to Microsoft.
The [0.3.33 Windows release](https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.3.33-windows)
is public and is the latest direct Antivirus release. Partner Center accepted
the validated `ZSEC-Antivirus-0.3.33.0-x64.msix` into Submission 4 and shows
**Update in certification**, with automatic publication after certification.
The live Store package remains 0.3.32.0 at this audit checkpoint; submission is
not certification or public availability of 0.3.33.0. Customer release notes and
reviewer instructions were updated to describe the compatibility change and the
remaining manual clean-device installation and upgrade acceptance checks.

The uploaded MSIX is 36,417,247 bytes with SHA-256
`fef4c46c0d95887fa153e292d9e359b5694ee0c0cf590485c2415adb1cf98f5f`.
Its 1,086 runtime files match the fresh direct payload. The public direct ZIP is
33,860,318 bytes with SHA-256
`2613a665949187747ecfa38d202361a80a44b736e87fa1d9e2ae30e2d6ada1de`;
its actual downloaded bytes, CRC and 1,107 manifest entries were verified.
Original 0.3.32 release assets were retained.

## Source and package evidence

- **TalkToAi Code:** fresh Windows installer and portable payload, all 23 packaged
  self-test checks passed, isolated Qt preview passed, and all 55 project-owned
  frozen modules matched the reviewed Store executable after source-filename
  normalization. Original source suite: 560 discovered, 547 passed, 13 skipped.
  Public installer/source archive hashes matched downloaded release files. The
  direct installer is unsigned and was not executed.
- **Portable source repair:** the expanded cross-platform tests discovered a
  missing-keyring bug affecting unauthenticated self-hosted endpoints. The stable
  [8.5.0 portable source repair](https://github.com/ResearchForumOnline/TalkToAi-Code/releases/tag/v8.5.0-portable.1)
  preserves the reviewed Windows tag/assets. [Ubuntu and macOS checks](https://github.com/ResearchForumOnline/TalkToAi-Code/actions/runs/36747048491)
  passed: each platform ran 451 tests, 446 passed and five skipped. Local full
  source suite: 568 discovered, 555 passed, 13 skipped. Windows key-storage policy
  is unchanged. The patched source archive has 228 exact Git files and 227 verified
  manifest hashes.
- **ZERO ONE:** Windows x64, macOS Apple Silicon and Linux x64 direct downloads
  are published with checksums. [Current desktop CI](https://github.com/ResearchForumOnline/ZERO-ONE-Desktop/actions/runs/36740617390)
  passed. Source, Store package and direct assets retain their separate provenance
  and installation boundaries in the linked release QA record.
- **ZSEC Browser:** 267 native assertions, 55 extension tests and 74 focused Python
  checks passed. The fresh native build's 32 app files matched the reviewed Store
  payload. Packaging was corrected to retain the login compatibility module and
  applicable license notices. [Release-source CI](https://github.com/ResearchForumOnline/ZSEC-Shield/actions/runs/36743378825)
  and CodeQL passed. Direct community binaries are unsigned.
- **ZSEC Antivirus:** the clean public Windows package passed 43 packaging tests,
  the unchanged 301-test suite plus 14 subtests, synthetic CLI/quarantine checks,
  PE identity checks and all 1,107 archived manifest hashes. Its public ZIP was
  downloaded and verified. Of 39 project code units, 38 matched the retained Store
  build; the public intelligence module contains a later Ubuntu/livepatch fix.
  This is recorded in the release receipt rather than described as a byte-identical
  Store binary.

## Free static website and signed updates

[TalkToAI](https://talktoai.org/) was updated through the existing free Cloudflare
Pages project. The reviewed production upload contained 81 files, 27 HTML pages
and 400 checked internal references with zero local validation errors. Its ZIP
SHA-256 was `0e106c52b44f81b2bcd399ed749999e98983767edc49ae06e59fa52c2a0c2856`.
Publication text now describes confirmed Store versions, and privacy and download
pages no longer describe those updates as awaiting publication.

Three scoped HTTPS redirects restore existing ZSEC update, intelligence and rule
paths to the existing signed GitHub Pages publisher. Product and privacy pages
remain on the static site. This uses supported [Cloudflare Pages redirects](https://developers.cloudflare.com/pages/configuration/redirects/),
retains client signature/expiry/rollback verification and avoids deploying a
snapshot that would expire after a week. No signing key was copied or changed.

The [signed publisher](https://github.com/ResearchForumOnline/ZSEC-Shield/actions/runs/36745852394)
completed sequence 60, advertising Antivirus 0.3.32 with the exact release ZIP
hash. Real client downloads and pinned-signature verification passed through the
canonical application and rule URLs. A separate compatibility problem was
identified: the complete intelligence feed is 2,379,423 bytes, exceeding the
current downloader's 2 MiB cap despite the intelligence verifier's 8 MiB cap.
Redirects alone do not resolve that client limit; its compatibility fix must have
separate version and validation evidence.

Antivirus 0.3.33 supplies that fix. A dedicated intelligence transport has a fixed
8 MiB maximum, while the existing public application/rules transport retains
its 2 MiB maximum and application metadata still has its 64 KiB verification
limit. Signature verification, expiry, rollback resistance, credential-free
HTTPS, bounded redirects and last-known-good retention remain enforced.
The patch passed 327 tests plus 14 subtests, Ruff and mypy; large valid,
oversized, tampered, expired and rollback cases are covered. The
[release-source CI](https://github.com/ResearchForumOnline/ZSEC-Shield/actions/runs/36751698775)
and [final publication-documentation CI](https://github.com/ResearchForumOnline/ZSEC-Shield/actions/runs/36752849970)
passed.

The [next protected signed publisher](https://github.com/ResearchForumOnline/ZSEC-Shield/actions/runs/36752105431)
completed sequence 61, advertising exact 0.3.33 release metadata. Canonical
talktoai.org application, intelligence and rule endpoints matched the GitHub
mirror byte for byte and passed the unchanged bundled pinned-key, digest,
expiry and signed-audit checks. The actual packaged client installed all 1,648
advisories into disposable test state. The notice remains notification-only;
automatic executable installation is disabled. Sequence 61 expires on
7 October 2026 at 17:33:24 UTC and is maintained by the existing publisher,
rather than a copied static snapshot. The advisory refresh failed closed, so
the publisher reused the complete last validated catalog; this is not a claim
that every advisory source was refreshed. See the
[public signed verification receipt](https://github.com/ResearchForumOnline/ZSEC-Shield/blob/main/docs/releases/ZSEC_SIGNED_FEED_SEQUENCE_61.json).

## Other current public work

- [OpenZero 7.3.0](https://github.com/ResearchForumOnline/OpenZero/releases/tag/v7.3.0):
  independent self-hosted runtime and optional operator-configured peers;
  [current checks passed](https://github.com/ResearchForumOnline/OpenZero/actions/runs/36729485623).
- [ZeroThink Local 1.0.0](https://github.com/ResearchForumOnline/ZeroThink/releases/tag/v1.0.0):
  standalone local research engine and ZERO ONE integration;
  [current checks passed](https://github.com/ResearchForumOnline/ZeroThink/actions/runs/36729858029).
- [ZMath Local 1.1.0](https://github.com/ResearchForumOnline/ZMath/releases/tag/v1.1.0):
  preserved public encryption work and local dual-key vault;
  [current checks passed](https://github.com/ResearchForumOnline/ZMath/actions/runs/36729396046).
- [Research preservation release](https://github.com/ResearchForumOnline/research/releases/tag/project-preservation-2026-09-30):
  original formatted papers and the five-repository offline kit. Those archives
  remain dated construction-time snapshots. Later release audits and index edits
  do not rewrite archived source or original research rights.

These checks establish the recorded software and release outcomes. They do not
establish manual clean-device installation, sustained model quality or independent
scientific or cryptographic certification.
