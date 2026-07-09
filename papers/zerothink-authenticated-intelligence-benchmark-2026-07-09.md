# ZeroThink Authenticated Intelligence Benchmark

Run date: 2026-07-09

Benchmark target: https://zerothink.talktoai.org/api_agent.php

Authorized account: redacted ZeroThink admin account

This benchmark tested ZeroThink as an authenticated model-routing layer. It used a temporary bearer token for the authorized ZeroThink account and the provider keys already saved to that account. Provider keys stayed server-side; they were not printed, exported, or committed.

ZeroTrade sources and credentials were explicitly excluded.

## Headline Result

On this 10-item exact-answer reasoning suite, the authenticated ZeroThink account routed cloud provider lanes successfully and exposed a tuning gap in the local OpenZero lanes.

| Lane | Model selected | Correct | Accuracy | Avg latency seconds |
| --- | --- | ---: | ---: | ---: |
| Groq via ZeroThink account key | `openai/gpt-oss-120b` | 10/10 | 100% | 0.850 |
| OpenAI via ZeroThink account key | `gpt-5.4` | 10/10 | 100% | 1.204 |
| Gemini via ZeroThink account key | `gemini-3.5-flash` | 10/10 | 100% | 3.272 |
| NVIDIA via ZeroThink account key | `meta/llama-3.3-70b-instruct` | 7/10 | 70% | 29.482 |
| ZeroThink/OpenZero GLM4 chat lane | `glm4:9b-q5` | 3/10 | 30% | 8.494 |
| ZeroThink/OpenZero Spectra8 chat lane | `spectra8-q8` | 3/10 | 30% | 75.703 |

Machine-readable outputs:

- [CSV results](../data/benchmarks/zerothink-authenticated-intelligence-benchmark-2026-07-09.csv)
- [Summary JSON](../data/benchmarks/zerothink-authenticated-intelligence-benchmark-summary-2026-07-09.json)
- [Targeted Spectra8 follow-up CSV](../data/benchmarks/zerothink-authenticated-intelligence-benchmark-2026-07-09-spectra8-only.csv)
- [Targeted Spectra8 follow-up JSON](../data/benchmarks/zerothink-authenticated-intelligence-benchmark-summary-2026-07-09-spectra8-only.json)

## What Was Tested

The suite used ten objective exact-answer prompts covering arithmetic, temporal reasoning, quantifier logic, sorting, Python expression evaluation, inventory arithmetic, structured JSON output, time arithmetic, a density trick question, and the classic mislabeled-boxes puzzle.

The scorer accepted the final answer even when a model included short extra text. It did not use an LLM judge. The benchmark is therefore reproducible and conservative, but it is not a substitute for MMLU, GSM8K, HumanEval, GPQA, SWE-bench, or human preference evaluation.

## Availability Findings

The saved ZeroThink account had usable keys for Groq, OpenAI, Gemini, NVIDIA, Serper, and ZeroThink/OpenZero during the run.

Two lanes were not scored:

| Lane | Availability result |
| --- | --- |
| xAI via ZeroThink account key | Unavailable: saved xAI key was rejected by the provider as incorrect |
| ZeroThink/OpenZero agent lane | Unavailable: local OpenZero agent runtime timed out and reported a self-heal cycle |

Perplexity was not included because this ZeroThink account path did not expose a Perplexity key/provider lane.

## Important Interpretation

This benchmark does **not** show ZeroThink beating OpenAI, Gemini, or Groq on raw model intelligence. The cloud lanes scored 10/10 because ZeroThink successfully routed requests to those saved-provider keys and models.

The meaningful ZeroThink result is architectural:

- authenticated account routing worked
- saved provider keys stayed server-side
- temporary benchmark tokens were revoked after the run
- no key/token leak patterns were detected in benchmark outputs
- cloud provider lanes reached strong exact-answer scores through ZeroThink
- the local OpenZero lanes were measurable and exposed a real tuning gap

The local OpenZero finding matters. `spectra8-q8` previously scored 9/10 in the direct OpenZero API model benchmark. In this authenticated ZeroThink route, the Spectra8 lane scored 3/10, with several 90-second local runtime timeouts and probe/context contamination. That means the model artifact and the ZeroThink wrapper path should be treated separately: Spectra8 can perform strongly through direct OpenZero, while the current ZeroThink/OpenZero serving path needs prompt/context/runtime cleanup before it should be promoted as equivalent.

Before the targeted Spectra8 follow-up, ZeroThink's OpenZero allow-list was updated to include the `spectra8-q8` route. The result therefore reflects an enabled ZeroThink/Spectra8 route, not a skipped or unsupported model.

## Task-Level Notes

The strongest account-routed lanes were Groq, OpenAI, and Gemini, each scoring 10/10. Groq was also the fastest of the perfect-score lanes in this run.

NVIDIA answered 7/10 but showed provider-side resource exhaustion on one item and missed two reasoning items.

ZeroThink/OpenZero GLM4 answered sorting, syllogism, and density correctly but missed arithmetic, calendar offset, Python range, inventory arithmetic, JSON reversal, time arithmetic, and mislabeled boxes.

ZeroThink/OpenZero Spectra8 answered arithmetic, sorting, and Python range correctly. It timed out on several items and produced verbose internal-style output on others, which points to route/runtime behavior rather than a clean direct-model comparison.

## Security And Cleanup

The benchmark scanned outputs for token-shaped OpenZero, OpenAI, Groq, Google, NVIDIA, ZeroThink CLI/API, and bearer-secret patterns. Rows with secret hits: 0.

Temporary benchmark tokens for the authorized account were revoked after the run. A cleanup query also confirmed zero active benchmark tokens remained.

## Relationship To Earlier Benchmarks

Use this benchmark for authenticated ZeroThink routing behavior and exact-answer results through the live ZeroThink API.

Use the separate Spectra/OpenZero benchmark for direct OpenZero model quality. In that earlier direct OpenZero suite, `spectra8-q8:latest` scored 9/10.
