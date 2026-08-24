"""Carga perezosa y compartida del modelo spaCy usado por todo `core/`."""

import spacy

_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("es_core_news_sm")
    return _nlp
