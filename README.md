# Kaihou Engine – Precise Translation

![Version 0.2.0](https://img.shields.io/badge/version-0.2.0-blue)
*One‑shot installer added, Spanish model support, live debug logs*

Kaihou Engine is a translation engine that combines linguistic analysis, LLMs, terminologies, dictionaries, guides, and any additional resources you add, to deliver precise, context‑aware translations.

## Core Capabilities
- Linguistic analysis (syntax, morphology, entities) via the internal `kaihou_engine.nlp_engine` implementation.
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
.
├─ .github/                # CI & publishing workflows
├─ config/                 # YAML config for models, pipeline, glossary, plugins
│   ├─ models.yaml
│   ├─ pipeline.yaml
│   ├─ glossaries/
│   └─ plugins.yaml
├─ src/                    # Python package source
│   └─ kaihou_engine/
│       └─ nlp_engine/      # internal NLP implementation
├─ tests/                  # test suite
├─ pyproject.toml
├─ README.md
├─ install.sh               # one‑shot installer (creates .venv, installs deps, spaCy models)
├─ requirements.txt          # placeholder – runtime deps are in pyproject.toml
├─ kaihou_spec.md
├─ LICENSE
```


## Installation
```bash
# Clone the repository
git clone https://github.com/kaihouproject/kaihou-engine.git
cd kaihou-engine

# Run the one‑shot installer (creates .venv, installs the package and spaCy models)
./install.sh

# Activate the virtual environment
source .venv/bin/activate
```

The installer automatically initializes any submodules (none are required now) and installs the required spaCy language models (`en`, `fr`, `es`).

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

[![CI](https://github.com/kaihouproject/kaihou-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/kaihouproject/kaihou-engine/actions/workflows/ci.yml)

## License
MIT License

Kaihou Engine is my personal playground for exploring NLP work—feel free to test it and contribute.
