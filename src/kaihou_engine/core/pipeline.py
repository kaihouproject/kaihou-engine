"""Pipeline implementation for Kaihou Engine.

The pipeline loosely follows the high‑level flow described in
``kaihou_spec.md`` (section 7).  For the initial version we implement a
single‑LLM (draft) path with optional validation plugins.  The design is
modular so additional steps (multi‑LLM panel, adaptive mode, correction
loop) can be added later.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..core.exceptions import PipelineError
from pydantic import ValidationError

from ..core.schemas import SourceAnalysis, TranslationRequest, LLMDraft, ValidationReport, TerminologyContext

from ..plugins.base import LLMConnectorPlugin

from ..plugins.plugin_registry import load_plugins

# ---------------------------------------------------------------------------
# Helper to run the external ``kaihou-nlp-engine`` CLI and obtain a parsed model.
# ---------------------------------------------------------------------------

def _run_nlp_engine(input_text: str, lang: str) -> SourceAnalysis:
    """Run the internal NLP analyzer (``nlp_engine.analyzer.analyze``) and return a ``SourceAnalysis`` model.
    """
    try:
        from kaihou_engine.nlp_engine.analyzer import analyze as nlp_analyze
        return nlp_analyze(input_text, lang)
    except Exception as exc:
        raise PipelineError(f"Failed to run internal NLP analyzer: {exc}")


# ---------------------------------------------------------------------------
# Core pipeline function used by the CLI.
# ---------------------------------------------------------------------------

def run_translation_pipeline(
    *,
    source_text: str,
    source_lang: str,
    target_lang: str,
    config_path: Path | None = None,
) -> Tuple[Dict[str, Any], List[ValidationReport]]:
    """Run the full translation pipeline and return a JSON‑serialisable dict.

    The returned dict mirrors the ``TranslationRequest`` plus the final
    translation and a flag indicating whether a multi‑LLM panel was used.
    ``validation_reports`` contains the individual validator results.
    """
    # 1️⃣ Load configuration (currently only used for future extension).
    # For now we ignore it – the default behaviour is hard‑coded.
    if config_path:
        # In a full implementation we would parse pipeline steps here.
        pass

    # 2️⃣ Load plugins (registry returns instances keyed by import path).
    plugins = load_plugins()

    # 3️⃣ NLP analysis (source)
    source_analysis = _run_nlp_engine(source_text, source_lang)

    # 4️⃣ Terminology context – use the GlossaryPlugin (if present) to provide terminology data.
    glossary_plugin = plugins.get("kaihou_engine.plugins.terminology.glossary_plugin.GlossaryPlugin")
    if glossary_plugin:
        terminology_context = glossary_plugin.query(source_analysis, None)
    else:
        terminology_context = TerminologyContext(terminology_hits=[], dictionary_entries=[], cultural_notes=[], regional_variant=None)
    # Convert to the expected ``TerminologyContext`` model (already a model if from plugin).
    terminology = terminology_context if isinstance(terminology_context, TerminologyContext) else TerminologyContext.model_validate(terminology_context)

    # 5️⃣ Build the translation request model
    request = TranslationRequest(
        source_text=source_text,
        source_lang=source_lang,
        target_lang=target_lang,
        analysis=source_analysis,
        terminology=terminology,
        instructions=[],
    )

    # Store debug info (source analysis and request) for optional output
    debug_info = {
        "source_analysis": source_analysis.model_dump(),
        "request": request.model_dump(),
    }

    # 6️⃣ Choose LLM connectors
    # Gather all LLMConnectorPlugin instances
    llm_connectors = [p for p in plugins.values() if isinstance(p, LLMConnectorPlugin)]
    if not llm_connectors:
        raise PipelineError("No LLM connector plugin found for translation")

    # Determine whether to run panel mode (multiple LLMs) from config
    # For now we read a simple flag from the optional pipeline config file
    use_panel = False
    if config_path and config_path.is_file():
        from ..core.config import load_yaml_file
        cfg = load_yaml_file(config_path)
        use_panel = cfg.get("use_panel", False)

    if use_panel:
        # Run all draft LLMs concurrently
        async def _run_all():
            return await asyncio.gather(*[c.translate(request) for c in llm_connectors])
        drafts = asyncio.run(_run_all())
        # Try to find a decider plugin (role "decider")
        decider = next((p for p in llm_connectors if getattr(p, "role", "") == "decider"), None)
        if decider:
            decision = asyncio.run(decider.decide(request, drafts))
            final_translation = decision.final_translation
            llm_used = [d.llm_id for d in drafts]
            used_panel = True
        else:
            # Fallback: pick first draft
            final_translation = drafts[0].translated_text
            llm_used = [drafts[0].llm_id]
            used_panel = True
    else:
        # Single draft – pick the first connector
        draft_connector = llm_connectors[0]
        async def _translate_one():
            return await draft_connector.translate(request)
        draft = asyncio.run(_translate_one())
        final_translation = draft.translated_text
        llm_used = [draft.llm_id]
        used_panel = False

    # 8️⃣ Assemble final output dict (including raw draft info)
    output: Dict[str, Any] = {
        "source_text": source_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "translation": final_translation,
        "llm_used": llm_used,
        "used_panel": used_panel,
        "debug": debug_info,
    }


    # No glossary substitution step (handled by TerminologyPlugin if needed).

    # 🔟 Validation – run each validator plugin and collect reports.
    validation_reports: List[ValidationReport] = []
    for plugin in plugins.values():
        from ..plugins.base import ValidatorPlugin
        if isinstance(plugin, ValidatorPlugin):
            report = plugin.validate(request, _run_nlp_engine(output["translation"], target_lang))
            validation_reports.append(report)

    output["validation"] = {
        "passed": all(r.passed for r in validation_reports),
        "issues": [issue.dict() for r in validation_reports for issue in r.issues],
    }
    return output, validation_reports


__all__ = ["run_translation_pipeline"]
