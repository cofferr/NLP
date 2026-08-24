"""POS tagging y lematización por documento."""

from core.nlp_model import get_nlp


def pos_lemma(text: str) -> list[dict]:
    doc = get_nlp()(text)
    return [
        {"text": token.text, "pos": token.pos_, "lemma": token.lemma_}
        for token in doc
    ]


def pos_lemma_batch(texts: list[str]) -> list[list[dict]]:
    return [pos_lemma(t) for t in texts]
