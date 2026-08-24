"""Visualización de dependencias sintácticas como SVG (displaCy)."""

from spacy import displacy

from core.nlp_model import get_nlp


def render_dependencies(text: str) -> str:
    doc = get_nlp()(text)
    return displacy.render(doc, style="dep", page=True)
