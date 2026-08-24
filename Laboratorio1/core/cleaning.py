"""Limpieza de texto: minúsculas, sin puntuación, sin stopwords, tildes/ñ/dígitos intactos."""

from core.nlp_model import get_nlp


def clean_text(text: str) -> str:
    doc = get_nlp()(text.lower())
    tokens = [
        token.text
        for token in doc
        if not token.is_punct and not token.is_space and not token.is_stop
    ]
    return " ".join(tokens)


def clean_texts(texts: list[str]) -> list[str]:
    return [clean_text(t) for t in texts]
