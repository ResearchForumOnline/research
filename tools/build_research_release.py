#!/usr/bin/env python3
"""
Build the public ResearchForumOnline/research release from the public
research.talktoai.org forum.

The script is intentionally dependency-free so it can run on a normal server
or workstation. It does not log secrets, does not require forum credentials,
and only reads public pages.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import re
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://research.talktoai.org"
BOARD = f"{BASE}/research-papers/"
USER_AGENT = "ResearchForumOnline public corpus builder/1.0 (+https://github.com/ResearchForumOnline/research)"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=35) as res:
        raw = res.read()
        charset = res.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


def strip_html(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"</p\s*>", "\n\n", fragment, flags=re.I)
    fragment = re.sub(r"<img[^>]+src=\"([^\"]+)\"[^>]*>", r"\n[image: \1]\n", fragment, flags=re.I)
    fragment = re.sub(r"<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>", lambda m: f"{strip_html(m.group(2)).strip()} ({html.unescape(m.group(1))})", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<script.*?</script>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<style.*?</style>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    text = html.unescape(fragment)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def slugify(value: str, max_len: int = 78) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-") or "untitled"
    return value[:max_len].rstrip("-")


def board_urls() -> list[str]:
    return [BOARD] + [f"{BOARD}{offset}/" for offset in range(20, 140, 20)]


def parse_topics(board_html: str) -> list[dict]:
    topics: list[dict] = []
    blocks = re.findall(r'<div class="windowbg[^"]*".*?</div><!-- \$topic\[css_class\] -->', board_html, flags=re.S)
    for block in blocks:
        title_match = re.search(r'<div class="message_index_title">.*?<a href="([^"]+)">(.*?)</a>', block, flags=re.S)
        if not title_match:
            continue
        starter_match = re.search(r"Started by\s*<a[^>]*>(.*?)</a>", block, flags=re.S)
        stats_match = re.search(r"Replies:\s*([^<]+)<br>Views:\s*([^<]+)", block, flags=re.S)
        date_match = re.search(r'<div class="lastpost">\s*<p><a href="[^"]+">([^<]+)</a>', block, flags=re.S)
        title = strip_html(title_match.group(2))
        href = html.unescape(title_match.group(1))
        topics.append(
            {
                "title": title,
                "url": href,
                "starter": strip_html(starter_match.group(1)) if starter_match else "",
                "replies": strip_html(stats_match.group(1)) if stats_match else "",
                "views": strip_html(stats_match.group(2)) if stats_match else "",
                "last_post": strip_html(date_match.group(1)) if date_match else "",
            }
        )
    return topics


def parse_first_post(topic_html: str) -> tuple[str, str]:
    title_match = re.search(r"<title>(.*?)</title>", topic_html, flags=re.S)
    title = strip_html(title_match.group(1)) if title_match else "Untitled"
    post_match = re.search(
        r'<div class="inner" data-msgid="(\d+)" id="msg_\d+">\s*(.*?)\s*</div>\s*</div><!-- \.post -->',
        topic_html,
        flags=re.S,
    )
    if not post_match:
        post_match = re.search(r'<div class="inner"[^>]*id="msg_\d+">\s*(.*?)\s*</div>', topic_html, flags=re.S)
        body = strip_html(post_match.group(1)) if post_match else ""
    else:
        body = strip_html(post_match.group(2))
    return title, body


SPAM_TERMS = {
    "trolleybus",
    "te.ua",
    "schedule",
    "маршрут",
    "тролейб",
}


def classify_source(item: dict) -> dict:
    starter = (item.get("starter") or "").lower()
    text = f"{item.get('title','')} {item.get('text','')}".lower()
    support_authored = starter in {"support", "admin", "shafaet", "shaf", "zero"}
    likely_spam = any(term in text for term in SPAM_TERMS)
    third_party = not support_authored
    if likely_spam:
        lane = "excluded-likely-spam"
    elif support_authored:
        lane = "primary-shaf-corpus"
    else:
        lane = "third-party-forum-source"
    return {
        "support_authored": support_authored,
        "likely_spam": likely_spam,
        "third_party": third_party,
        "publication_lane": lane,
    }


def crawl() -> list[dict]:
    seen: set[str] = set()
    topics: list[dict] = []
    for url in board_urls():
        page = fetch(url)
        for topic in parse_topics(page):
            canonical = topic["url"].split("#", 1)[0]
            if canonical in seen:
                continue
            seen.add(canonical)
            topics.append(topic)
        time.sleep(0.1)

    enriched: list[dict] = []
    for idx, topic in enumerate(topics, 1):
        try:
            html_page = fetch(topic["url"])
            page_title, text = parse_first_post(html_page)
        except urllib.error.URLError as exc:
            page_title, text = topic["title"], f"[crawl error: {exc}]"
        source_id = f"rfo-{idx:03d}-{slugify(topic['title'], 48)}"
        row = {
            "id": source_id,
            "title": topic["title"] or page_title,
            "url": topic["url"],
            "starter": topic.get("starter", ""),
            "replies": topic.get("replies", ""),
            "views": topic.get("views", ""),
            "last_post": topic.get("last_post", ""),
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "word_count": len(re.findall(r"\w+", text)),
            "excerpt": textwrap.shorten(text.replace("\n", " "), width=900, placeholder="..."),
            "text": text,
        }
        row.update(classify_source(row))
        enriched.append(row)
        time.sleep(0.08)
    return enriched


def source_themes(sources: list[dict]) -> dict[str, list[dict]]:
    themes = {
        "zero-boundary-algebra": ["zero", "boundary", "0,-0,+0", "mathematics", "probability"],
        "zerothink-reasoning": ["zerothink", "reasoning", "sovereign", "agent", "lattice"],
        "openzero-local-ai": ["openzero", "local", "node", "sovereign", "hive"],
        "zmath-shield-security": ["zmath", "encryption", "shield", "secure", "vault"],
        "quantum-evidence": ["quantum", "ionq", "qiskit", "simulator", "evidence"],
        "bio-dna-organic-computing": ["dna", "genetic", "organic", "human body", "bio"],
        "ethics-probability-goodness": ["goodness", "ethics", "moral", "alignment", "probability"],
        "botanical-research": ["clove", "oregano", "turmeric", "pain", "antimicrobial", "formula"],
        "ai-research-workflow": ["research", "paper", "professor zero", "co-scientist", "survey"],
    }
    out: dict[str, list[dict]] = {key: [] for key in themes}
    primary = [s for s in sources if s["publication_lane"] == "primary-shaf-corpus"]
    for source in primary:
        hay = f"{source['title']} {source['text'][:2500]}".lower()
        for theme, terms in themes.items():
            if any(term in hay for term in terms):
                out[theme].append(source)
    return out


def source_rows(items: list[dict], limit: int = 10) -> str:
    rows = []
    for src in items[:limit]:
        rows.append(f"- `{src['id']}`: {src['title']} — {src['url']} ({src['publication_lane']}, {src['word_count']} words crawled)")
    return "\n".join(rows) if rows else "- No direct forum source matched this theme; treat as a synthesis gap."


DOMAIN_NOTES = {
    "zero-boundary-algebra-provenance-workflow.md": {
        "lens": "This lane should be read as notation and workflow control. The symbols and transition labels can help organise reset states, polarity shifts, source states, and decision points. The publishable claim is not that standard mathematics has been replaced; the publishable claim is that a local notation can improve traceability when paired with ordinary audit logs.",
        "methods": [
            "Define the notation vocabulary in a glossary that maps every non-standard symbol to an ordinary explanation.",
            "Run a before/after audit task where researchers annotate the same note set with and without the notation.",
            "Measure whether claim provenance, contradiction spotting, and revision planning become easier for a reviewer.",
        ],
        "risk": "Readers may reject mystical or absolute wording. Keep the paper anchored in notation, provenance, and workflow effects.",
    },
    "zerothink-sovereign-reasoning-layer.md": {
        "lens": "This lane is strongest when ZeroThink is presented as a research operating layer: intake, source status, claim mapping, draft generation, critique, and export. The important distinction is between a language model producing fluent prose and a workflow forcing the model output through evidence gates.",
        "methods": [
            "Compare a normal one-shot LLM answer with a staged ZeroThink paper-creator run on the same seed articles.",
            "Score hallucinated citations, unsupported claims, missing limitations, and reviewer usefulness.",
            "Publish anonymised examples where the staged process catches weak claims before the final draft.",
        ],
        "risk": "Do not claim the system guarantees truth. Claim that it makes evidence status more visible and easier to challenge.",
    },
    "openzero-local-first-ai-nodes.md": {
        "lens": "This lane is about practical sovereignty: local inference, CPU-friendly models, optional web or voice tools, and service bridges that still work when hosted APIs are unavailable. The research value is cost, control, continuity, and inspectable deployment.",
        "methods": [
            "Benchmark response latency and throughput on CPU-only hardware with several model sizes.",
            "Record what tasks work locally, what needs external tools, and what fails gracefully.",
            "Compare privacy and operational cost against a hosted-only assistant pattern.",
        ],
        "risk": "Avoid implying local models outperform all hosted models. The stronger claim is resilience and control.",
    },
    "zmath-shield-evidence-containers.md": {
        "lens": "This lane should stay at the public behaviour level: encrypted container, metadata boundary, entitlement policy, user-owned secrets, and verifier behaviour. The paper should never expose proprietary source code, keys, or implementation tricks.",
        "methods": [
            "Publish a threat model and public container fields without publishing private encryption implementation.",
            "Test tampering, wrong password, wrong pattern, revoked licence, and offline/online policy behaviour.",
            "Invite third-party review of the public claims and implementation boundary.",
        ],
        "risk": "Security must not depend on secrecy alone. Use standard primitives and treat closed code as IP protection, not the proof of security.",
    },
    "quantum-ready-evidence-graphs.md": {
        "lens": "This lane is a research PoC, not a production-certified quantum document reader. AI extracts claims and evidence; classical baselines and quantum/simulator candidate methods are tested only on constrained optimisation problems such as path selection and clustering.",
        "methods": [
            "Create a claim graph from public documents and assign confidence, contradiction, and provenance weights.",
            "Run classical baseline algorithms for evidence-path selection and clustering.",
            "Run simulator or quantum-cloud candidate methods only as optimisation experiments, then compare quality, cost, and reproducibility.",
        ],
        "risk": "Do not claim quantum computers understand documents or that a provider endorses the system. The measurable object is optimisation behaviour.",
    },
    "probability-of-goodness-ethical-routing.md": {
        "lens": "This lane is best framed as a governance heuristic. A Probability of Goodness score can be tested as an explicit routing signal for agent actions, escalation, refusal, review, or evidence gathering.",
        "methods": [
            "Define a transparent rubric for good, harmful, uncertain, and needs-review outcomes.",
            "Run the rubric on historical prompts and compare with human reviewer decisions.",
            "Track false positives, false negatives, delay cost, and user trust.",
        ],
        "risk": "Do not present a moral score as universal truth. Present it as a configurable audit heuristic.",
    },
    "bio-digital-research-boundaries.md": {
        "lens": "This lane must stay careful. DNA, health, ancestry, and organic-computing themes can be explored as interpretation workflows, but public outputs should avoid diagnosis, treatment advice, ethnicity certainty, or ancestry proof claims.",
        "methods": [
            "Separate raw-file quality checks from health research notes and lineage storytelling.",
            "Use public databases only through their documented evidence labels and update cycles.",
            "Have a reviewer flag any wording that sounds clinical, deterministic, or identity-defining.",
        ],
        "risk": "Health and genetics claims are high-stakes. Require expert review before stronger wording is used.",
    },
    "botanical-formula-research-roadmap.md": {
        "lens": "This lane can be valuable if it is reframed as safety-first experimental design. Botanical notes become literature-search seeds, extraction variables, hazard checks, and lab-study questions rather than public treatment instructions.",
        "methods": [
            "Build a source ledger for each ingredient, claimed effect, dose range, and contraindication.",
            "Separate in-vitro evidence, animal evidence, human evidence, traditional use, and anecdote.",
            "Require safety review before any human-use language appears.",
        ],
        "risk": "Avoid medical advice. Use the roadmap to ask what would need to be tested, not to recommend use.",
    },
    "research-forum-corpus-synthesis-2026.md": {
        "lens": "The umbrella lane turns the forum into a map: what exists, what is original, what is speculative, what can be turned into software documentation, and what needs external validation before publication.",
        "methods": [
            "Maintain a public source ledger and a private-source exclusion policy.",
            "Group source papers by research lane, product lane, and high-risk claim lane.",
            "Create a review queue that upgrades the strongest drafts first.",
        ],
        "risk": "A corpus synthesis can become too broad. Keep each future paper tied to a focused question and a small source set.",
    },
}


def domain_note(slug: str) -> dict:
    return DOMAIN_NOTES.get(slug, DOMAIN_NOTES["research-forum-corpus-synthesis-2026.md"])


def paper_front_matter(title: str, slug: str, themes: list[str]) -> str:
    today = dt.date.today().isoformat()
    theme_yaml = "[" + ", ".join(json.dumps(t) for t in themes) + "]"
    return f"---\ntitle: {json.dumps(title)}\ndate: {today}\nstatus: \"working paper generated with ZeroThink Paper Creator protocol\"\nsource: \"research.talktoai.org public forum corpus\"\nthemes: {theme_yaml}\n---\n\n# {title}\n\n"


def build_paper(title: str, slug: str, thesis: str, theme_keys: list[str], themes: dict[str, list[dict]]) -> str:
    matched: list[dict] = []
    seen: set[str] = set()
    for key in theme_keys:
        for source in themes.get(key, []):
            if source["id"] not in seen:
                seen.add(source["id"])
                matched.append(source)
    primary_titles = "; ".join(src["title"] for src in matched[:5]) or "the public Research Forum Online corpus"
    note = domain_note(slug)
    method_rows = "\n".join(f"{idx}. {item}" for idx, item in enumerate(note["methods"], 1))
    related_links = ""
    if slug == "quantum-ready-evidence-graphs":
        related_links = """
Related public workflow pages:

- QuantumEncryption1 Paper Creator evidence workflow: https://quantumencryption1.com/paper-creator-evidence-workflow/
- Quantum-ready evidence workflow: https://quantumencryption1.com/quantum-evidence-workflow/
- ZeroThink Paper Creator: https://zerothink.talktoai.org/research-paper-creator
- TalkToAI ecosystem: https://talktoai.org/
- CallChat ZERO secure communication lane: https://callchat.org/

"""
    body = paper_front_matter(title, slug, theme_keys)
    body += f"""## Plain-Language Summary

This working paper turns the public Research Forum Online corpus into a cleaner research draft. It does not claim institutional approval, clinical proof, government certification, or quantum advantage. It treats the forum posts as a source corpus, then uses the ZeroThink Paper Creator method: source ledger first, claim graph second, synthesis third, and limitations visible at the end.

{related_links}
## Abstract

{thesis} The source base is drawn from public forum papers including {primary_titles}. The contribution is a structured research direction rather than a finished peer-reviewed finding: it identifies reusable concepts, separates evidence from speculation, and proposes validation tasks that can be run with ordinary classical baselines before any quantum, simulator, or AI-agent extension is treated as meaningful.

## 1. Research Question

How can the ideas in the Research Forum Online corpus be converted into a publishable, auditable research programme without overstating what has been experimentally demonstrated?

## 2. Source-Ledger Basis

{source_rows(matched, 12)}

The forum posts are treated as originating research notes and concept papers. They are useful for extracting vocabulary, design intent, and hypotheses. They are not automatically treated as external validation. Where a claim would normally require a peer-reviewed citation, dataset, benchmark, lab protocol, or reproducible experiment, this paper marks it as a validation task.

## 3. Claim/Evidence/Provenance Graph

| Claim ID | Claim | Evidence source | Provenance status | Confidence |
| --- | --- | --- | --- | --- |
| C1 | The corpus contains a coherent recurring design language around sovereignty, local control, reasoning layers, and evidence trails. | Multiple primary forum posts listed above. | Public forum source, concept-level evidence. | Medium |
| C2 | The corpus can be reframed into safer academic language by separating product claims, hypotheses, protocols, and speculative interpretations. | ZeroThink Paper Creator protocol and source-ledger method. | Methodological synthesis. | High |
| C3 | Some claims require experimental support before public-sector, medical, or security deployment wording is justified. | Claims involving health, encryption assurance, quantum validation, or autonomous agents. | Needs external validation. | High |
| C4 | A provenance-aware workflow can make the work more fundable and reviewable because it preserves what came from notes, what came from retrieved sources, and what came from model inference. | Research Paper Creator / Nottingham lane design. | Internal method plus public workflow design. | Medium |

Graph edges: `source note -> extracted concept -> claim -> evidence status -> validation task -> revised paper section`.

## 4. Synthesis

The strongest publishable direction is not to ask readers to accept every forum claim as already proven. The stronger route is to present the body of work as a research programme: a set of models, tools, hypotheses, and implementation lanes that can be tested in public, reproducible ways. This keeps the originality visible while making the work easier for developers, supervisors, universities, funders, and technical reviewers to evaluate.

### Domain-Specific Lens

{note["lens"]}

The repeated pattern across the corpus is a preference for systems that keep agency close to the user: local AI nodes, audit trails, user-controlled vault files, visible evidence ledgers, and careful boundaries between public behaviour and private implementation. That pattern can be formalised as a design principle:

> A sovereign AI system should make its claims inspectable, its control boundaries explicit, and its private material unnecessary for public verification.

This principle lets the work speak to multiple domains. In AI research, it becomes a method for agent accountability. In security, it becomes an argument for verifiable envelope design rather than secret-algorithm claims. In education, it becomes a student-facing workflow for turning rough notes into defensible literature reviews. In product design, it becomes a way to explain why local-first systems and hosted systems can co-exist.

## 5. Validation Plan

General validation rules:

1. Build a source ledger from every public research note and mark each row as primary note, external paper, retrieved result, product page, or needs verification.
2. Convert each major claim into a testable form.
3. For software claims, publish installation steps, screenshots, API responses, and failure cases.
4. For security claims, publish threat models, key boundaries, and third-party review targets without exposing proprietary keys or private encryption source.
5. For health or biological claims, avoid advice language and require literature review, safety review, and professional framing before public claims are strengthened.
6. For quantum or simulator claims, compare against a classical baseline and state what the quantum job actually proves: job execution, optimisation experiment, or telemetry record, not magical cognition.

Theme-specific validation tasks:

{method_rows}

## 6. Limitations

The present draft is generated from a public forum crawl and a ZeroThink-style synthesis protocol. It is not peer reviewed. It does not verify every historic claim in the corpus. It does not expose private ZMath, ZeroThink, OpenZero, server, or API-key material. It is suitable as a working-paper foundation, a grant appendix starter, or a student survey-expansion example after human review.

Specific caution for this lane: {note["risk"]}

## 7. Next Research Step

The next step is a two-pass evidence upgrade: first, map each claim to external scholarly or technical sources; second, run a reviewer-style critique that removes claims that cannot be supported. That gives the work a credible route from invention notes to academic paper, product white paper, or reproducible demonstration.

## Appendix A: Candidate Source Rows

{source_rows(matched, 30)}
"""
    return body


def generated_papers(themes: dict[str, list[dict]]) -> dict[str, str]:
    specs = [
        (
            "zero-boundary-algebra-provenance-workflow.md",
            "Zero Boundary Algebra as a Provenance Workflow for AI Research Notes",
            "This paper reframes Zero Boundary Algebra as a practical provenance and transition-notation layer for research workflows rather than as a claim that replaces established mathematics.",
            ["zero-boundary-algebra", "ai-research-workflow"],
        ),
        (
            "zerothink-sovereign-reasoning-layer.md",
            "ZeroThink as a Sovereign Reasoning Layer: From Rough Notes to Auditable Research",
            "This paper describes ZeroThink as a research workflow that can separate prompts, source ledgers, claim graphs, drafts, critiques, and exports.",
            ["zerothink-reasoning", "ai-research-workflow", "ethics-probability-goodness"],
        ),
        (
            "openzero-local-first-ai-nodes.md",
            "OpenZero and Local-First AI Nodes for Low-Cost Sovereign Agents",
            "This paper positions OpenZero as a local-first AI node pattern where CPU-friendly inference, optional web/voice tools, and visible operator controls reduce dependence on closed hosted systems.",
            ["openzero-local-ai", "zerothink-reasoning"],
        ),
        (
            "zmath-shield-evidence-containers.md",
            "ZMath Shield and Portable Evidence Containers: A Public Behaviour Specification",
            "This paper describes the public behaviour of a protected file-container layer while keeping proprietary implementation details out of the public release.",
            ["zmath-shield-security", "zero-boundary-algebra"],
        ),
        (
            "quantum-ready-evidence-graphs.md",
            "Quantum-Ready Evidence Graphs for Claim Selection, Clustering, and Auditability",
            "This paper proposes a cautious PoC workflow where AI builds claim/evidence graphs and quantum or simulator methods are tested only on constrained optimisation tasks.",
            ["quantum-evidence", "ai-research-workflow", "zmath-shield-security"],
        ),
        (
            "probability-of-goodness-ethical-routing.md",
            "Probability of Goodness as an Ethical Routing Heuristic for Agentic Systems",
            "This paper turns the Probability of Goodness material into a bounded agent-governance heuristic that can be evaluated through routing decisions and audit logs.",
            ["ethics-probability-goodness", "zero-boundary-algebra", "zerothink-reasoning"],
        ),
        (
            "bio-digital-research-boundaries.md",
            "Bio-Digital Research Boundaries for DNA, Organic Computing, and AI Interpretation",
            "This paper turns the biological and DNA-themed corpus into a cautious research-boundary document that separates interpretation, hypothesis, and clinical evidence.",
            ["bio-dna-organic-computing", "ai-research-workflow"],
        ),
        (
            "botanical-formula-research-roadmap.md",
            "Botanical Formula Research Roadmap: From Forum Notes to Safe Experimental Design",
            "This paper reframes botanical antimicrobial and pain-relief notes as a safety-first experimental design roadmap, not a medical recommendation.",
            ["botanical-research", "ai-research-workflow"],
        ),
        (
            "research-forum-corpus-synthesis-2026.md",
            "Research Forum Online Corpus Synthesis 2026",
            "This umbrella paper maps the public forum corpus into themes, source-ledger rules, publication lanes, and next review tasks.",
            list(themes.keys()),
        ),
    ]
    return {filename: build_paper(title, filename, thesis, keys, themes) for filename, title, thesis, keys in specs}


def write_release(sources: list[dict]) -> None:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    for rel in ["data", "sources", "papers", "docs", "templates", "tools"]:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)
    public_sources = [{k: v for k, v in src.items() if k != "text"} for src in sources]
    (ROOT / "data" / "research-forum-source-index.json").write_text(json.dumps({
        "generated_at": now,
        "source_site": BASE,
        "board": BOARD,
        "source_count": len(sources),
        "primary_shaf_corpus_count": sum(1 for s in sources if s["publication_lane"] == "primary-shaf-corpus"),
        "third_party_count": sum(1 for s in sources if s["publication_lane"] == "third-party-forum-source"),
        "excluded_likely_spam_count": sum(1 for s in sources if s["publication_lane"] == "excluded-likely-spam"),
        "sources": public_sources,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    ledger_lines = [
        "# Research Forum Source Ledger",
        "",
        f"Generated: {now}",
        "",
        "This ledger indexes the public `research.talktoai.org` research-paper board. Full forum text is not republished here; the repo uses titles, URLs, excerpts, hashes, and generated working papers.",
        "",
        "Publication lanes:",
        "",
        "- `primary-shaf-corpus`: started by support/admin-like account and suitable as the main Shaf/TalkToAI source corpus.",
        "- `third-party-forum-source`: public forum material started by another user; cite carefully and do not treat as owned research.",
        "- `excluded-likely-spam`: likely spam/noise, kept in the data index for audit but excluded from synthesis.",
        "",
        "| ID | Lane | Title | Starter | Words | URL |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for src in sources:
        title = src["title"].replace("|", "\\|")
        ledger_lines.append(f"| `{src['id']}` | {src['publication_lane']} | {title} | {src['starter']} | {src['word_count']} | {src['url']} |")
    (ROOT / "sources" / "research-forum-source-ledger.md").write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")

    theme_map = source_themes(sources)
    for filename, content in generated_papers(theme_map).items():
        (ROOT / "papers" / filename).write_text(content, encoding="utf-8")

    template = """# ZeroThink Paper Creator Public Protocol

Use this protocol for public research drafting:

1. Start with a topic and research question.
2. Build a source ledger before drafting.
3. Label provenance as uploaded source, user note, retrieved search result, full text supplied, model candidate lead, or needs verification.
4. Build a claim/evidence/provenance graph.
5. Draft only after the evidence map exists.
6. Add reviewer critique and revision tasks.
7. Keep speculative, clinical, quantum, security, and government wording cautious unless external evidence supports stronger claims.

Public routes:

- QuantumEncryption1 Paper Creator evidence workflow: https://quantumencryption1.com/paper-creator-evidence-workflow/
- Quantum-ready evidence workflow: https://quantumencryption1.com/quantum-evidence-workflow/
- ZeroThink Paper Creator: https://zerothink.talktoai.org/research-paper-creator
- TalkToAI ecosystem: https://talktoai.org/
- CallChat ZERO secure communication lane: https://callchat.org/

This public protocol does not include private ZeroThink prompts, private ZMath encryption implementation, keys, server configuration, or proprietary source code.
"""
    (ROOT / "templates" / "zerothink-paper-creator-public-protocol.md").write_text(template, encoding="utf-8")

    guide = """# Student Guide: Survey Expansion With ZeroThink Paper Creator

Students can use the paper creator to expand a survey or literature review from a small set of articles:

Useful public routes:

- Start with the QuantumEncryption1 guide: https://quantumencryption1.com/paper-creator-evidence-workflow/
- Run the live tool in ZeroThink Paper Creator: https://zerothink.talktoai.org/research-paper-creator
- Use the wider TalkToAI hub for project context: https://talktoai.org/
- Use CallChat for secure communication and Shield licensing context: https://callchat.org/

1. Collect seed papers, abstracts, notes, or DOIs.
2. Upload or paste them into the Research Paper Creator.
3. Run the literature-search plan stage.
4. Run the evidence-plan stage.
5. Build a claim/evidence/provenance graph.
6. Use the source ledger to separate verified sources from candidate leads.
7. Draft the survey expansion.
8. Run reviewer critique.
9. Revise manually before submission.

The quantum/simulator lane is only for constrained optimisation tasks such as evidence-path selection, clustering, routing, prioritisation, and auditability scoring. It is not a claim that quantum computers understand papers.
"""
    (ROOT / "docs" / "student-survey-expansion-guide.md").write_text(guide, encoding="utf-8")

    boundary = """# Public Release Boundary

This repository publishes research papers, source ledgers, and public workflows.

It must not contain:

- private ZMath or CallChat Shield implementation code
- ZeroThink private prompts or keys
- API keys, SSH keys, database credentials, or server passwords
- raw private DNA, vault, chat, customer, or payment data
- exploit instructions or operational details useful for attacking live services

Security and encryption papers describe public behaviour, threat models, and validation plans only.
"""
    (ROOT / "PUBLIC_RELEASE_BOUNDARY.md").write_text(boundary, encoding="utf-8")

    readme = f"""# ResearchForumOnline Research

Public research-paper releases generated from the public [Research Forum Online]({BASE}) corpus using the ZeroThink Paper Creator method.

This repo is designed for clean, citeable public work:

- source-ledger first
- claim/evidence graph before synthesis
- careful academic wording
- no private ZMath, ZeroThink, server, or key material
- generated working papers ready for human review

## Public Workflow Links

- [TalkToAI ecosystem](https://talktoai.org/) - public project hub, course, docs, and product routes.
- [CallChat ZERO](https://callchat.org/) - Matrix-compatible secure communication and Shield licensing lane.
- [QuantumEncryption1 Paper Creator evidence workflow](https://quantumencryption1.com/paper-creator-evidence-workflow/) - student and research workflow for survey expansion, source ledgers, and claim/evidence/provenance graphs.
- [Quantum-ready evidence workflow](https://quantumencryption1.com/quantum-evidence-workflow/) - controlled PoC lane for provenance graphs and classical versus simulator/quantum optimisation tests.
- [ZeroThink Paper Creator](https://zerothink.talktoai.org/research-paper-creator) - live research-paper drafting tool.

## New Working Papers

| Paper | Focus |
| --- | --- |
| [Zero Boundary Algebra as a Provenance Workflow](papers/zero-boundary-algebra-provenance-workflow.md) | Public mathematical/workflow framing |
| [ZeroThink as a Sovereign Reasoning Layer](papers/zerothink-sovereign-reasoning-layer.md) | Research writing and audit workflow |
| [OpenZero and Local-First AI Nodes](papers/openzero-local-first-ai-nodes.md) | CPU-friendly sovereign agents |
| [ZMath Shield and Portable Evidence Containers](papers/zmath-shield-evidence-containers.md) | Public behaviour spec, no private encryption code |
| [Quantum-Ready Evidence Graphs](papers/quantum-ready-evidence-graphs.md) | AI claim graphs plus constrained optimisation tests |
| [Probability of Goodness](papers/probability-of-goodness-ethical-routing.md) | Ethical routing heuristic |
| [Bio-Digital Research Boundaries](papers/bio-digital-research-boundaries.md) | DNA/organic computing caution lane |
| [Botanical Formula Research Roadmap](papers/botanical-formula-research-roadmap.md) | Safety-first research plan |
| [Research Forum Corpus Synthesis 2026](papers/research-forum-corpus-synthesis-2026.md) | Umbrella map of the corpus |

## Source Ledger

- [Research Forum Source Ledger](sources/research-forum-source-ledger.md)
- [Machine-readable source index](data/research-forum-source-index.json)

## How The Papers Were Built

The generator crawls public forum pages, indexes first-post text, filters likely spam/noise, marks third-party posts separately, then applies the public ZeroThink Paper Creator protocol.

Run:

```bash
python tools/build_research_release.py
```

## Safety Boundary

Read [PUBLIC_RELEASE_BOUNDARY.md](PUBLIC_RELEASE_BOUNDARY.md) before adding material. This repo is public research text only. It does not publish proprietary encryption code, private prompts, keys, credentials, customer data, or live-server internals.
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    sources = crawl()
    write_release(sources)
    print(json.dumps({
        "source_count": len(sources),
        "primary_shaf_corpus_count": sum(1 for s in sources if s["publication_lane"] == "primary-shaf-corpus"),
        "third_party_count": sum(1 for s in sources if s["publication_lane"] == "third-party-forum-source"),
        "excluded_likely_spam_count": sum(1 for s in sources if s["publication_lane"] == "excluded-likely-spam"),
    }, indent=2))


if __name__ == "__main__":
    main()
