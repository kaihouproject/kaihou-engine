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

## Alternative Distribution Methods

You can install *Kaihou Engine* without publishing to PyPI using any of the following approaches:

### 1. Direct install from GitHub (editable)
```bash
# Clone the repository (or just point pip to the URL)
python -m pip install -e git+https://github.com/kaihouproject/kaihou-engine.git@main#egg=kaihou-engine
```
This installs the package in editable mode, so you can modify the source and the changes are reflected immediately.

### 2. Install from a GitHub Release (wheel)
1. Create a release on GitHub (e.g., `v0.2.0`). The CI workflow will build a wheel and attach it as an asset.
2. Download the wheel asset and install it locally:
```bash
curl -L -o kaihou_engine-0.2.0-py3-none-any.whl \
    https://github.com/kaihouproject/kaihou-engine/releases/download/v0.2.0/kaihou_engine-0.2.0-py3-none-any.whl
python -m pip install kaihou_engine-0.2.0-py3-none-any.whl
```

### 3. Install from GitHub Packages (private or public registry)
If you enable GitHub Packages for the repository, you can publish the wheel there and install it with:
```bash
python -m pip install \
    --extra-index-url https://npm.pkg.github.com/kaihouproject \
    kaihou-engine
```
You will need a personal access token with the `read:packages` scope stored in `~/.pypirc` or passed via environment variables.

These alternatives let you distribute the engine without needing an account on PyPI.

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

## Acknowledgements

The Kaihou Engine stands on the shoulders of many great open‑source projects and the broader Python community:

- **[spaCy](https://spacy.io/)** – the NLP library that provides the linguistic backbone.
- **[Rich](https://github.com/Textualize/rich)** – beautiful terminal rendering and colorised output.
- **[Click](https://palletsprojects.com/p/click/)** – the CLI framework that powers our command line.
- **[Python](https://www.python.org/)** – for its extensive ecosystem and thriving community.
- And countless **contributors** who have helped improve Kaihou Engine.

These items are tracked in the GitHub milestone **Future Features**.

[![CI](https://github.com/kaihouproject/kaihou-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/kaihouproject/kaihou-engine/actions/workflows/ci.yml)

## License
MIT License

Kaihou Engine is my personal playground for exploring NLP work—feel free to test it and contribute.
