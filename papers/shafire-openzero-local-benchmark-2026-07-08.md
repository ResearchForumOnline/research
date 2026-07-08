# Shafire and OpenZero Local Benchmark Snapshot

Date: 2026-07-08

This is a first public benchmark snapshot for selected `shafire` Hugging Face models and the live OpenZero CPU node. It is intentionally modest: a reproducible exact-answer smoke benchmark, not a replacement for HELM, lm-eval, Open LLM Leaderboard, MMLU, GSM8K, GPQA, or AIME.

## Key Findings

- `shafire/talktoai` and `shafire/talktoaiZERO` were created on Hugging Face on 2024-09-09, three days before OpenAI's public `o1-preview` announcement on 2024-09-12.
- The narrower defensible historical claim is: early TalkToAI/talktoaiZERO public artifacts predate the public OpenAI o1-preview "thinking before responding" release. This does not mean reasoning research or chain-of-thought prompting did not exist before then.
- `shafire/talktoaiQT`, `shafire/talktoaiQ`, AgentZero, and the Spectra family came after the o1-preview announcement but before DeepSeek-R1, except `Spectra8`, which was created after DeepSeek-R1 and is based on DeepSeek-R1-Distill-Llama-8B.
- `talktoaizero-q6:latest`, installed from `shafire/talktoaiZERO` on the OpenZero server during this run, scored 7/10 on the exact-answer suite with 4.096s average latency.
- On the same suite, the strongest installed comparison models were `gemma3:12b` and `hermes3:8b-llama3.1-q5_K_M`, both at 8/10.

## Release Timeline Context

| Artifact | Public date | Why it matters |
| --- | ---: | --- |
| Meta Llama 3.1 | 2024-07-23 | Base family used by the first TalkToAI Llama 3.1 fine-tunes. |
| `shafire/talktoai` | 2024-09-09 | Early TalkToAI Llama 3.1 8B Instruct fine-tune. |
| `shafire/talktoaiZERO` | 2024-09-09 | Public TalkToAI ZERO quantized/fine-tuned artifact. |
| OpenAI o1-preview | 2024-09-12 | Public OpenAI release framed around models spending more time thinking before responding. |
| `shafire/talktoaiQT` | 2024-09-14 | Later TalkToAI quantum/thinking themed fine-tune. |
| `shafire/talktoaiQ` | 2024-09-19 | Later GGUF-oriented TalkToAIQ/SkynetZero artifact. |
| AgentZero / AgentZeroLLM | 2024-10-02 to 2024-10-08 | Gemma-2-9B-it based AgentZero line. |
| SpectraMind family | 2024-11-13 onward | CPU-oriented GGUF bundle and Spectra variants. |
| DeepSeek-R1 | 2025-01-20 | Open reasoning model release with DeepThink/R1 positioning. |
| `shafire/Spectra8` | 2025-02-09 | Built from DeepSeek-R1-Distill-Llama-8B, so it is post-R1. |

Sources:

- Hugging Face API snapshot: [`data/benchmarks/shafire-huggingface-models-2026-07-08.json`](../data/benchmarks/shafire-huggingface-models-2026-07-08.json)
- Meta Llama 3.1 release: https://ai.meta.com/blog/meta-llama-3-1/
- Llama 3.1 8B Instruct model card: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
- OpenAI o1-preview announcement: https://openai.com/index/introducing-openai-o1-preview/
- DeepSeek-R1 announcement: https://api-docs.deepseek.com/news/news250120

## Benchmark Method

Environment:

- OpenZero live CPU node, reported as 6 CPU cores and 20 GB RAM.
- OpenZero version: 5.4.0.
- API route: OpenAI-compatible `/v1/chat/completions`.
- Runtime: Ollama through OpenZero.
- `openzero_spark`: `off`.
- Temperature: `0`.
- Max tokens requested: `64`.

Task:

- 10 compact exact-answer prompts across arithmetic, simple logic, and basic science.
- Prompt asked for final answer only.
- Scoring is exact/contains-match against accepted final answers.
- Verbose answers that did not reach the final answer inside the response cap were counted as misses. This intentionally measures instruction following as well as raw reasoning.

Data:

- Per-question CSV: [`data/benchmarks/openzero-api-exact-answer-2026-07-08.csv`](../data/benchmarks/openzero-api-exact-answer-2026-07-08.csv)
- Summary JSON: [`data/benchmarks/openzero-api-exact-answer-summary-2026-07-08.json`](../data/benchmarks/openzero-api-exact-answer-summary-2026-07-08.json)

## Results

| Model | Correct | Accuracy | Avg latency seconds | Notes |
| --- | ---: | ---: | ---: | --- |
| `gemma3:12b` | 8/10 | 80% | 5.748 | Installed OpenZero comparison model. |
| `hermes3:8b-llama3.1-q5_K_M` | 8/10 | 80% | 7.505 | Installed OpenZero comparison model. |
| `talktoaizero-q6:latest` | 7/10 | 70% | 4.096 | Pulled from `shafire/talktoaiZERO` during this run. |
| `qwen2.5:1.5b` | 7/10 | 70% | 1.236 | Fastest successful comparison. |
| `qwen2.5:3b` | 7/10 | 70% | 1.617 | Fast comparison. |
| `glm4:9b-q5` | 6/10 | 60% | 9.966 | Active OpenZero model at start of run. |
| `gemma4:e4b` | 2/10 | 20% | 10.287 | Mostly blank responses through this route. |
| `gemma4:e2b` | 0/10 | 0% | 7.122 | Blank responses through this route. |

## Local GGUF Loader Note

A local Windows llama.cpp runner (`b9929`) was also tested before switching to the server. The small `shafire/talktoai-F16-GGUF` and `shafire/AgentZero-Q8_0-GGUF` files failed current llama.cpp loading with:

```text
error loading model hyperparameters: key not found in model: llama.context_length
```

Those files were therefore not scored. They likely need re-export to a current GGUF layout, or testing with the original-era runtime that accepted them.

## Interpretation

This run does not prove that TalkToAI/talktoaiZERO beat frontier models at release. It does show:

- the early public TalkToAI/talktoaiZERO artifacts predate public o1-preview by date;
- `talktoaiZERO` can be installed and served on the current OpenZero CPU node;
- on a small strict exact-answer suite, `talktoaiZERO` is competitive with the installed Qwen 1.5B/3B comparisons and below the best installed Hermes/Gemma3 comparison models;
- OpenZero needs a larger benchmark harness next: GSM8K subset, ARC-Challenge subset, MMLU-Pro or MMLU subset, and a long-form qualitative reasoning set with judged rubrics.

## Security Observation

During benchmarking, the live OpenZero `/api/config` response exposed sensitive operator fields. Public reports must not include those values. The server should rotate exposed credentials and adjust `/api/config` to return only safe public status fields.
