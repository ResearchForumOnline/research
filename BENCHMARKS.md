# Benchmark Results

This page indexes public benchmark snapshots for Shafire, TalkToAI, Spectra, and OpenZero model work.

## 2026-07-09: ZeroThink Authenticated Intelligence Benchmark

Latest authenticated ZeroThink intelligence benchmark:

- [ZeroThink Authenticated Intelligence Benchmark](papers/zerothink-authenticated-intelligence-benchmark-2026-07-09.md)
- [Scored CSV](data/benchmarks/zerothink-authenticated-intelligence-benchmark-2026-07-09.csv)
- [Summary JSON](data/benchmarks/zerothink-authenticated-intelligence-benchmark-summary-2026-07-09.json)

Headline result on the 10-item exact-answer suite:

| Lane | Model | Correct | Accuracy |
| --- | --- | ---: | ---: |
| Groq via ZeroThink account key | `openai/gpt-oss-120b` | 10/10 | 100% |
| OpenAI via ZeroThink account key | `gpt-5.4` | 10/10 | 100% |
| Gemini via ZeroThink account key | `gemini-3.5-flash` | 10/10 | 100% |
| NVIDIA via ZeroThink account key | `meta/llama-3.3-70b-instruct` | 7/10 | 70% |
| ZeroThink/OpenZero GLM4 chat lane | `glm4:9b-q5` | 3/10 | 30% |
| ZeroThink/OpenZero Spectra8 chat lane | `spectra8-q8` | 3/10 | 30% |

Important limitation: this benchmark shows authenticated ZeroThink routing behavior, not ZeroThink beating frontier vendors on raw model intelligence. It also exposed a real tuning gap: direct OpenZero `spectra8-q8:latest` scored 9/10 in the earlier model benchmark, while the current ZeroThink/OpenZero Spectra8 route scored 3/10 with timeouts/context contamination.

## 2026-07-09: ZeroThink Public System Benchmark

Latest ZeroThink system benchmark:

- [ZeroThink Public System Benchmark](papers/zerothink-system-benchmark-2026-07-09.md)
- [Scored CSV](data/benchmarks/zerothink-system-benchmark-2026-07-09.csv)
- [Summary JSON](data/benchmarks/zerothink-system-benchmark-summary-2026-07-09.json)

Headline result on the public unauthenticated system/API suite:

| Area | Passed | Notes |
| --- | ---: | --- |
| Public pages | 6/6 | Live web routes returned expected pages and markers |
| CLI API | 6/6 | Device login, pending poll, input guards, and auth guards behaved correctly |
| Agent API | 4/4 | Unauthenticated generation was blocked; safe direct local identity/capability branches worked |
| Static integration markers | 7/7 | OpenZero routing, Paper Creator workflow, validators, and CLI protocol markers were present |
| Secret-leak scan | 0 hits | No token-shaped key/secret patterns appeared in benchmark responses |

Important limitation: this is a ZeroThink system-surface benchmark, not a full authenticated generation-quality leaderboard. The benchmark intentionally avoided account cookies, real provider keys, and private server credentials.

## 2026-07-08: Spectra8, TalkToAiQ, SpectraMind, and OpenZero

Latest benchmark page:

- [Spectra8, TalkToAiQ, and SpectraMind OpenZero Benchmark](papers/spectra-talktoaiq-openzero-benchmark-2026-07-08.md)
- [Scored CSV](data/benchmarks/openzero-spectra-talktoaiq-benchmark-2026-07-08.csv)
- [Summary JSON](data/benchmarks/openzero-spectra-talktoaiq-benchmark-summary-2026-07-08.json)
- [Hugging Face artifact snapshot](data/benchmarks/shafire-spectra-talktoaiq-artifacts-2026-07-08.json)

Headline result on the 10-question exact-answer CPU/API suite:

| Model | Correct | Accuracy | Avg latency seconds |
| --- | ---: | ---: | ---: |
| `spectra8-q8:latest` | 9/10 | 90% | 15.035 |
| `gemma3:12b` | 8/10 | 80% | 5.748 |
| `hermes3:8b-llama3.1-q5_K_M` | 8/10 | 80% | 7.505 |
| `talktoaizero-q6:latest` | 7/10 | 70% | 4.096 |
| `qwen2.5:1.5b` | 7/10 | 70% | 1.236 |
| `qwen2.5:3b` | 7/10 | 70% | 1.617 |
| `glm4:9b-q5` | 6/10 | 60% | 9.966 |
| `spectramind3-q8:latest` | 1/10 | 10% | 4.945 |
| `microspectramind-q8:latest` | 0/10 | 0% | 4.993 |
| `spectramindz-q8:latest` | 0/10 | 0% | 24.830 |
| `talktoaiq-f16:latest` | 0/10 | 0% | 43.258 |

Important limitation: several SpectraMind/TalkToAiQ variants loaded but mostly echoed the OpenZero API system prompt instead of answering. Those are reported as served-model/template failures on this route, not proof that the underlying training data has no value. Just need to do further tests on the failed parts i got ai to do it for me took hours, so time consuming.

## 2026-07-08: TalkToAI ZERO Initial Snapshot

- [Shafire and OpenZero Local Benchmark Snapshot](papers/shafire-openzero-local-benchmark-2026-07-08.md)
- [Scored CSV](data/benchmarks/openzero-api-exact-answer-2026-07-08.csv)
- [Summary JSON](data/benchmarks/openzero-api-exact-answer-summary-2026-07-08.json)
- [Shafire Hugging Face model snapshot](data/benchmarks/shafire-huggingface-models-2026-07-08.json)
