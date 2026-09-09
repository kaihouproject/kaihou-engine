"""Command‑line interface for the internal NLP analyzer.

Usage example (mirrors the original submodule):

    python -m kaihou_engine.nlp_engine.cli analyze <file> -l en --json
"""

from __future__ import annotations

import json
from pathlib import Path
import click

from .analyzer import analyze

@click.group()
def cli() -> None:
    pass

@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("-l", "--lang", "lang", required=True, help="Language code (en, fr, …)")
@click.option("--json", "as_json", is_flag=True, default=False, help="Print JSON output")
def analyze_cmd(path: Path, lang: str, as_json: bool) -> None:
    """Analyze *path* with spaCy and optionally output JSON."""
    text = path.read_text(encoding="utf-8")
    result = analyze(text, lang)
    if as_json:
        click.echo(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
    else:
        click.echo(f"Language: {result.language}\nTokens: {len(result.tokens)}\nEntities: {len(result.entities)}")

if __name__ == "__main__":
    cli()
