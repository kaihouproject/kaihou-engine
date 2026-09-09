# Kaihou Engine – Precise Translation

Kaihou Engine is a translation engine that combines linguistic analysis, LLMs, terminologies, dictionaries, guides, and any additional resources you add, to deliver precise, context‑aware translations.

## Core Capabilities
- Linguistic analysis (syntax, morphology, entities) via `kaihou-nlp-engine`.
- Terminology and glossary enforcement.
- Validation of numbers, entities, terminology, and semantic similarity.
- Self‑correcting loop: failing drafts are sent back to the LLM for revision.
- Multi‑LLM panel with optional decider to choose the best draft.

## Architecture Overview

```
Source text
   │
   ▼
kaihou‑nlp‑engine ──▶ Linguistic analysis (syntax, morphology, entities)
   │
   ▼
Terminology / Glossary lookup
   │
   ▼
LLM(s) ──▶ Draft translation(s)
   │
   ▼
LLM Decider (optional, when several LLMs are used) ──▶ Chosen draft
   │
   ▼
kaihou‑nlp‑engine ──▶ Re‑analysis of the draft
   │
   ▼
Validation (numbers, entities, terminology, semantic similarity)
   ├── Failure ──▶ LLM‑based correction ──▶ Re‑validation (loop)
   └── Success ──▶ Final translation output
```

## Repository Layout

```
kaihou-engine/
├─ .github/                # CI \u0026 publishing workflows
├─ config/
│   ├─ models.yaml          # LLM profiles (connector, strengths, etc.)
│   ├─ pipeline.yaml        # Order of steps, thresholds, adaptive‑mode rules
│   ├─ glossaries/          # Domain‑specific term glossaries (YAML)
│   └─ plugins.yaml         # List of enabled plugins (by module path)
├─ src/kaihou_engine/
│   ├─ __init__.py
│   ├─ orchestrator.py      # CLI entry point (`kaihou` console script)
│   ├─ core/                # Pipeline runner, schemas, exceptions
│   └─ plugins/             # LLM connectors, terminologists, validators, etc.
├─ .gitignore
├─ pyproject.toml
└─ README.md                # (this file)
```

## Installation
```bash
git clone https://github.com/houtarou-d/kaihou-engine.git
cd kaihou-engine
git submodule update --init   # fetch kaihou-nlp-engine
pip install -e ./kaihou-engine[dev]
```

## Quick Start
```bash
# Interactive menu
kaihou translate

# One‑shot command (JSON output)
kaihou translate --text "Bonjour le monde" --from fr --to en --json
```

## Configuration
YAML files in `config/` define models, pipeline steps, glossaries, and enabled plugins.

## Contribution
We welcome contributions. Open a pull request (forking is optional) and reference the related issue; the maintainer will review it promptly.

## Future Work
- Sentiment analysis integration
- Style/tonality detection
- Additional language pairs (e.g., ES, DE)
- Plug‑in for remote LLM APIs

These items are tracked in the GitHub milestone **Future Features**.

[![CI](https://github.com/houtarou-d/kaihou-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/houtarou-d/kaihou-engine/actions/workflows/ci.yml)

## License
MIT License

Kaihou Engine is my personal playground for exploring NLP work—feel free to test it and contribute.
