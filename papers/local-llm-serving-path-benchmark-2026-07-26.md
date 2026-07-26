# Separating Model Artifact Performance from Serving-Path Failure: A Small Reproducible Benchmark of Local LLM Routes

**Shafaet Brady Hussain**

Independent researcher, TalkToAI Research, United Kingdom

26 July 2026

## Abstract

Local language-model evaluations frequently conflate the behaviour of a model artifact with the behaviour of the application route that serves it. We report a small, reproducible exact-answer benchmark of eleven locally served models and variants through an OpenAI-compatible OpenZero/Ollama route. The protocol used ten objective prompts, temperature zero, a 64-token cap, and a deterministic exact/contains scoring rule. `spectra8-q8:latest` achieved 9/10 (90%) with 15.035 s mean latency; several other models scored 70–80%; three SpectraMind variants and one TalkToAiQ route scored 0–10% while frequently echoing application control text. The results demonstrate a serving-path compatibility signal, not a general intelligence ranking or evidence that any training corpus caused a result. The 10-item suite is too small for model ranking. Its primary contribution is methodological: preserve raw responses and distinguish model-artifact questions from wrapper, prompt-template, context, and runtime failures.

**Keywords:** local language models; reproducibility; model serving; prompt templates; benchmark methodology; OpenAI-compatible APIs

## 1. Introduction

Model benchmarks often report a single score for a system assembled from model weights, a runtime, a chat template, an API wrapper, and a client prompt. That score can conceal a critical engineering distinction: a model may fail because its artifacts are unsuitable, or because a serving path supplies incompatible control text, template tokens, or context. This study uses a deliberately small exact-answer suite to document that distinction in an operational local-AI setting.

The work evaluates a dated OpenZero/Ollama API route, not an abstract model family. It makes no claim that the highest-scoring local artifact is generally better than other models. Instead, it records a reproducible failure mode: some routes returned HTTP-successful responses while emitting system/control text rather than answers. Keeping those observations alongside scores is important for diagnosing deployed AI systems and aligns with calls to document model context and system-level technical debt [1–3].

## 2. Research questions

- **RQ1:** Under a fixed exact-answer protocol, what scores and latencies did the tested local routes produce?
- **RQ2:** Did HTTP-successful routes always yield task-directed answers?
- **RQ3:** What evidence distinguishes a likely serving/template compatibility issue from a model-quality conclusion?

## 3. Materials and method

### 3.1 Test snapshot

The benchmark was run on 8 July 2026 through the live OpenZero 5.4 CPU node using the OpenAI-compatible `/v1/chat/completions` interface. The released result set covers eleven named routes or prior-reference variants. The public project artifacts associated with the test include `shafire/Spectra8`, `shafire/TalkToAiQ`, and `shafire/SpectraMind`; the evaluation records artifact aliases, not a claim of causal provenance from a dataset to a score.

### 3.2 Protocol

Each route received the same ten exact-answer prompts spanning arithmetic, simple logic, and basic science. Temperature was zero and the maximum output length was 64 tokens. Scoring accepted the expected final answer when present; responses that failed to answer, echoed system/control text, or violated the requested answer format were scored as misses. Mean latency is arithmetic mean response time in seconds.

This is a diagnostic smoke benchmark. It is not MMLU, GSM8K, HumanEval, GPQA, HELM, or a human-preference study. Ten items cannot support a broad ranking, significance test, or capability claim.

### 3.3 Reproducibility and boundary

The scored CSV, JSON summary, raw response files, and runner reside in the public ResearchForumOnline research release. No account credentials or private production configuration are included. The data are a fixed historical snapshot; later releases must be measured and reported separately.

## 4. Results

**Table 1. Fixed-suite scores and mean latency.**

| Route | Correct / 10 | Accuracy | Mean latency (s) |
|---|---:|---:|---:|
| `spectra8-q8:latest` | 9 | 90% | 15.035 |
| `gemma3:12b` | 8 | 80% | 5.748 |
| `hermes3:8b-llama3.1-q5_K_M` | 8 | 80% | 7.505 |
| `talktoaizero-q6:latest` | 7 | 70% | 4.096 |
| `qwen2.5:1.5b` | 7 | 70% | 1.236 |
| `qwen2.5:3b` | 7 | 70% | 1.617 |
| `glm4:9b-q5` | 6 | 60% | 9.966 |
| `spectramind3-q8:latest` | 1 | 10% | 4.945 |
| `microspectramind-q8:latest` | 0 | 0% | 4.993 |
| `spectramindz-q8:latest` | 0 | 0% | 24.830 |
| `talktoaiq-f16:latest` | 0 | 0% | 43.258 |

The highest result was `spectra8-q8:latest`, with 9/10 under the restricted suite. The most important negative finding is that several low-scoring routes loaded and returned HTTP 200 yet commonly emitted OpenZero system/control text rather than task answers. An HTTP success code therefore did not establish useful inference behaviour.

## 5. Interpretation

The results support a narrow systems inference: wrapper and template behaviour is a measurable part of a locally served model system. For the routes that echoed control text, the immediate next experiment is not to declare a failed model. It is to run a direct Ollama prompt without the OpenZero wrapper, inspect the model-specific chat template, clear any injected context, and rerun a larger preregistered suite. This separates artifact behaviour from route behaviour and prevents a deployment bug from becoming an unsupported training-data claim.

The comparison is also useful operationally. Under this particular CPU/API setup, the fastest successful routes were the two Qwen variants, while the highest restricted-suite accuracy had a substantially longer mean latency. That is a deployment trade-off observation, not a universal Pareto frontier.

## 6. Limitations

- Ten prompts are inadequate for general capability ranking.
- Exact/contains scoring can miss partially correct or well-reasoned answers.
- The test did not control hardware, context-window configuration, quantization family, template, or concurrent load across all models.
- The results are dated and route-specific.
- The work does not establish safety, licensing status, training-data provenance, or suitability for any high-stakes use.
- The author is affiliated with the project ecosystem and reports this as a self-evaluation.

## 7. Conclusion

This benchmark records a useful engineering lesson: a local model route can return HTTP success while failing the task because of serving-path contamination. A transparent release should preserve those failures, the exact scoring rule, latencies, raw outputs, and a clear boundary between model artifact and deployment route. The findings justify further controlled testing; they do not justify broad performance claims.

## Data and code availability

Source data: `data/benchmarks/openzero-spectra-talktoaiq-benchmark-2026-07-08.csv` and `data/benchmarks/openzero-spectra-talktoaiq-benchmark-summary-2026-07-08.json` in https://github.com/ResearchForumOnline/research. The original benchmark note and public artifact snapshot are included in the same release.

## Conflict of interest and AI-use disclosure

The author builds components in the TalkToAI/OpenZero ecosystem. This is a self-evaluation, not an independent audit. AI-assisted drafting tools were used for editorial structuring; no generated statement is presented as a measurement without a released result artifact.

## References

1. Sculley D, et al. Hidden Technical Debt in Machine Learning Systems. *Advances in Neural Information Processing Systems 28*. 2015.
2. Mitchell M, et al. Model Cards for Model Reporting. *Proceedings of FAT\* 2019*. 2019. https://doi.org/10.1145/3287560.3287596
3. Liang P, et al. Holistic Evaluation of Language Models. *Transactions on Machine Learning Research*. 2023. https://doi.org/10.48550/arXiv.2211.09110
