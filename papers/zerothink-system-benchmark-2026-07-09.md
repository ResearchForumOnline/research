# ZeroThink Public System Benchmark

Run date: 2026-07-09

Benchmark target: https://zerothink.talktoai.org

This benchmark treats ZeroThink as a deployed web/API reasoning system rather than a single model file. The run checked public route availability, API guard behavior, CLI device-login behavior, safe direct-mode local replies, static integration markers in the local source checkout, and public response leakage for token-shaped secrets.

## Headline Result

ZeroThink passed all 23 benchmark checks.

| Area | Passed | Result |
| --- | ---: | --- |
| Public pages | 6/6 | Main site, Research Paper Creator, research/docs/FAQ, and CLI connect routes returned expected pages |
| CLI API | 6/6 | Missing-input guards, auth guards, device-start handshake, and pending poll state behaved correctly |
| Agent API | 4/4 | Unauthenticated generation was blocked; safe direct identity/capability local branches worked |
| Static integration markers | 7/7 | OpenZero routing, local model map, Paper Creator workflow markers, validators, and CLI protocol markers were present |
| Secret-leak scan | 0 hits | No token-shaped OpenZero, OpenAI, GitHub, Hugging Face, Google, bearer, or server-password patterns appeared in benchmark responses |

Machine-readable outputs:

- [CSV results](../data/benchmarks/zerothink-system-benchmark-2026-07-09.csv)
- [Summary JSON](../data/benchmarks/zerothink-system-benchmark-summary-2026-07-09.json)

## Live Route Timing

Each public page was requested three times. Mean latency below is seconds from the benchmark runner.

| Route | Statuses | Mean latency | Title observed |
| --- | --- | ---: | --- |
| `/` | 200, 200, 200 | 0.102 | ZeroThink \| Real Quantum AI & Sovereign Intelligence |
| `/research-paper-creator` | 200, 200, 200 | 0.083 | Research Paper Creator \| ZeroThink |
| `/research` | 200, 200, 200 | 0.074 | ZeroThink Research \| Real Quantum AI |
| `/faq` | 200, 200, 200 | 1.096 | ZeroThink \| System Documentation |
| `/docs` | 200, 200, 200 | 0.125 | Docs \| ZeroThink |
| `/cli/connect` | 200, 200, 200 | 0.054 | ZeroThink CLI Connect |

Overall benchmarked endpoint-row latency mean was 0.134 seconds, with a row median of 0.061 seconds.

## API Behavior Findings

`/api_agent.php` correctly blocked unauthenticated OpenZero generation with HTTP 403 and the expected JSON error status. The same guard also blocked an unsupported OpenZero direct-mode attempt, which is the desired public boundary because ZeroThink does not accept browser-supplied OpenZero URLs or keys for that lane.

Two safe direct-mode local branches were verified without real provider keys: `who are you?` returned the `zero-direct-identity` local reply, and `what can you do?` returned the `zero-direct-capabilities` local reply. These branches stop inside ZeroThink's local code before an external provider call, so the benchmark used a fake placeholder key only.

`/api_cli.php` exposed the expected CLI login protocol. The benchmark verified missing-action and missing-device-code guards, unauthenticated `me` and protected-action guards, a successful `device_start` handshake with device-login fields present, and an unapproved `device_poll` returning HTTP 202 `authorization_pending`.

## OpenZero Integration Markers

The local ZeroThink source checkout contains OpenZero integration markers for:

- `/v1/agent/runs`
- chat-completion fallback behavior
- `zt_openzero_agent_run_request`
- `zt_openzero_local_model_map`

The local OpenZero model map values detected in this checkout were:

- `glm4:9b-q5`
- `hermes3:8b-llama3.1-q5_K_M`
- `gemma4:e4b`

The source files hashed for this benchmark were:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `api_agent.php` | 135935 | `fdcdf8b61a020cf93b42c13d32dd91c36e2899bdde7c639722605839ca061dca` |
| `api_cli.php` | 5444 | `a161c484d28021091fde67d00ad3be31f5cb58ecd1c628c88dc788980e36f4a0` |
| `research-paper-creator.php` | 73950 | `f472979502edbd34f5d5b844ed239846ed68a49c45683cbcf44fadecd685d748` |

## Interpretation

This run shows that ZeroThink's public system surface is live, fast, guarded, and wired to the expected OpenZero and Paper Creator components. It is not a model-quality leaderboard entry by itself. The unauthenticated benchmark intentionally did not run paid/provider-backed generation or account-backed ZeroThink/OpenZero requests.

For model answer quality, use the separate OpenZero model benchmark snapshot. In that suite, `spectra8-q8:latest` scored 9/10 on the exact-answer CPU/API benchmark, ahead of the included OpenZero comparison models in that run.

## Limitations

No account cookies, real provider API keys, private server credentials, or hidden session state were used. Static-code checks were performed against the local source checkout, while the behavior checks were performed against the live public ZeroThink endpoint. A future authenticated benchmark can add full ZeroThink generation quality tests once a sanctioned test account or explicit session lane is prepared.
