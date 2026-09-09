"""Simple internal NLP analyzer used by Kaihou Engine.

We replace the external submodule with a tiny implementation based on spaCy.
It loads the appropriate language model (as defined in `config/models.yaml`) and
produces a `SourceAnalysis` object that matches the schema in
`kaihou_engine.core.schemas`.
"""

from __future__ import annotations

from pathlib import Path
import spacy




from kaihou_engine.core.schemas import SourceAnalysis, Token, NamedEntity

# Mapping from language code to spaCy model name – keep in sync with config/models.yaml
LANG_MODEL_MAP = {
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    "es": "es_core_news_sm",
    "de": "de_core_news_sm",
}




def _load_model(lang: str):
    model_name = LANG_MODEL_MAP.get(lang)
    if not model_name:
        raise ValueError(f"No spaCy model configured for language '{lang}'")
    try:
        return spacy.load(model_name)
    except OSError as exc:
        raise RuntimeError(
            f"spaCy model '{model_name}' not installed. Install it with: "
            f"python -m spacy download {model_name}"
        ) from exc


def analyze(text: str, lang: str) -> SourceAnalysis:
    """Run spaCy analysis on *text* for language *lang*.

    Returns a :class:`SourceAnalysis` compatible with the Kaihou schema.
    """
    nlp = _load_model(lang)
    doc = nlp(text)

    tokens: List[Token] = []
    for i, tok in enumerate(doc):
        tokens.append(
            Token(
                text=tok.text,
                lemma=tok.lemma_,
                pos=tok.pos_,
                tag=tok.tag_,
                morph=tok.morph.to_dict(),
                dep=tok.dep_,
                head_index=tok.head.i,
                index=i,
            )
        )

    entities: List[NamedEntity] = []
    for ent in doc.ents:
        # Filter out entities that are all lowercase (likely non‑named entities such as greetings)
        if ent.text.islower():
            continue
        entities.append(
            NamedEntity(
                text=ent.text,
                label=ent.label_,
                start_char=ent.start_char,
                end_char=ent.end_char,
            )
        )

    # For simplicity we treat the whole doc as a single sentence.
    sentences = [sent.text for sent in doc.sents]

    return SourceAnalysis(
        raw_text=text,
        language=lang,
        tokens=tokens,
        entities=entities,
        sentences=sentences,
        register=None,
        tone=None,
        domain=None,
    )
