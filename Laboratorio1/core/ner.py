"""Reconocimiento de entidades nombradas por documento."""

from core.nlp_model import get_nlp


def extract_entities(text: str) -> list[dict]:
    doc = get_nlp()(text)
    return [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
        for ent in doc.ents
    ]


def extract_entities_batch(texts: list[str]) -> list[list[dict]]:
    return [extract_entities(t) for t in texts]
