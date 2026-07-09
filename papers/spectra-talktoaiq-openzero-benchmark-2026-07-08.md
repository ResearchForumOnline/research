# Spectra8, TalkToAiQ, and SpectraMind OpenZero Benchmark

Date: 2026-07-08

This benchmark extends the first Shafire/OpenZero snapshot to the Hugging Face datasets and paired model artifacts requested for:

- `shafire/Spectra8`: https://huggingface.co/datasets/shafire/Spectra8
- `shafire/TalkToAiQ`: https://huggingface.co/datasets/shafire/TalkToAiQ
- `shafire/SpectraMind`: https://huggingface.co/datasets/shafire/SpectraMind

The matching model repositories tested through OpenZero were:

- `shafire/Spectra8` -> `spectra8-q8:latest`
- `shafire/talktoaiQ` -> `talktoaiq-f16:latest`
- `shafire/SpectraMind` -> `microspectramind-q8:latest`, `spectramind3-q8:latest`, and `spectramindz-q8:latest`

## Method

- Runtime: live OpenZero 5.4 CPU node, OpenAI-compatible `/v1/chat/completions` API.
- Backend: Ollama model aliases created from the public GGUF files.
- Temperature: `0`.
- Max tokens: `64`.
- Suite: 10 exact-answer prompts covering arithmetic, simple logic, and basic science.
- Scoring: exact/contains match for the final answer. Responses that did not answer, echoed the system prompt, or failed the requested final-answer format were scored as misses.

Raw public artifacts:

- [Scored CSV](../data/benchmarks/openzero-spectra-talktoaiq-benchmark-2026-07-08.csv)
- [Summary JSON](../data/benchmarks/openzero-spectra-talktoaiq-benchmark-summary-2026-07-08.json)
- [Hugging Face artifact snapshot](../data/benchmarks/shafire-spectra-talktoaiq-artifacts-2026-07-08.json)

## Results

| Model | Source | Correct | Accuracy | Avg latency seconds | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| `spectra8-q8:latest` | `shafire/Spectra8`, Q8 GGUF | 9/10 | 90% | 15.035 | Strongest result in this local suite. |
| `gemma3:12b` | Installed comparison | 8/10 | 80% | 5.748 | Strong comparison baseline. |
| `hermes3:8b-llama3.1-q5_K_M` | Installed comparison | 8/10 | 80% | 7.505 | Strong comparison baseline. |
| `talktoaizero-q6:latest` | Prior Shafire run | 7/10 | 70% | 4.096 | Included as prior Shafire/OpenZero reference. |
| `qwen2.5:1.5b` | Installed comparison | 7/10 | 70% | 1.236 | Fastest successful baseline. |
| `qwen2.5:3b` | Installed comparison | 7/10 | 70% | 1.617 | Fast successful baseline. |
| `glm4:9b-q5` | Active OpenZero comparison | 6/10 | 60% | 9.966 | Active model at the earlier benchmark start. |
| `spectramind3-q8:latest` | `shafire/SpectraMind`, 3B Q8 GGUF | 1/10 | 10% | 4.945 | Loaded, but often emitted prompt/control text. |
| `microspectramind-q8:latest` | `shafire/SpectraMind`, 1B Q8 GGUF | 0/10 | 0% | 4.993 | Loaded, but echoed OpenZero API system text. |
| `spectramindz-q8:latest` | `shafire/SpectraMind`, 8B Q8 GGUF | 0/10 | 0% | 24.830 | Loaded, but echoed OpenZero API system text. |
| `talktoaiq-f16:latest` | `shafire/talktoaiQ`, F16 GGUF | 0/10 | 0% | 43.258 | Loaded, but echoed OpenZero API system text and was slow on CPU. |

## Notes

`Spectra8` is the clear positive result here: it loaded through OpenZero/Ollama and scored 9/10 on the same strict exact-answer suite that the earlier `talktoaiZERO` run scored 7/10 on.

The poor SpectraMind and TalkToAiQ scores should be read carefully. The models were available in Ollama and returned HTTP 200 responses, but their outputs mostly repeated the OpenZero API system prompt or safety/control text instead of answering the questions. That is a serving/template compatibility problem on this route, and it should be retested with:

- a direct Ollama prompt path without the OpenZero API wrapper;
- a model-specific chat template or plain completion template;
- a larger benchmark suite after prompt-format repair.

## Artifact Inventory

The requested Hugging Face dataset repos are public and were captured in the artifact snapshot:

| Dataset | Created | Notes |
| --- | ---: | --- |
| `shafire/Spectra8` | 2025-06-13 | CSV dataset, fewer than 1K rows. |
| `shafire/TalkToAiQ` | 2025-06-13 | Multiple CSV training/reflection files. |
| `shafire/SpectraMind` | 2025-06-13 | Split CSV dataset, 100K to 1M row category. |

The paired model repos tested here were created earlier:

| Model repo | Created | Runnable file used |
| --- | ---: | --- |
| `shafire/Spectra8` | 2025-02-09 | `Spectra8-8.0B-Q8_0.gguf` |
| `shafire/talktoaiQ` | 2024-09-19 | `talktoaiQuantum.gguf` |
| `shafire/SpectraMind` | 2024-11-13 | `MicroSpectraMind_q8.gguf`, `SpectraMind3_q8.gguf`, `SpectraMindz_q8.gguf` |

## Next Benchmark Step

The next meaningful pass should use direct Ollama calls on the OpenZero server and bypass the API system wrapper for the models that echoed system text. That will separate model capability from route/template compatibility.
