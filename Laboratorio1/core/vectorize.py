"""Vectorización de documentos: vocabulario, one-hot, bag of words, TF-IDF."""

import math

from core.cleaning import clean_texts


def _tokenize_documents(documents: list[str]) -> list[list[str]]:
    cleaned = clean_texts(documents)
    return [doc.split() for doc in cleaned]


def build_vocabulary(tokenized_docs: list[list[str]]) -> list[str]:
    terms = {term for doc in tokenized_docs for term in doc}
    return sorted(terms)


def bag_of_words(tokenized_docs: list[list[str]], vocabulary: list[str]) -> list[list[int]]:
    index = {term: i for i, term in enumerate(vocabulary)}
    bow = []
    for doc in tokenized_docs:
        row = [0] * len(vocabulary)
        for term in doc:
            row[index[term]] += 1
        bow.append(row)
    return bow


def one_hot(tokenized_docs: list[list[str]], vocabulary: list[str]) -> list[list[list[int]]]:
    index = {term: i for i, term in enumerate(vocabulary)}
    result = []
    for doc in tokenized_docs:
        doc_vectors = []
        for term in doc:
            vector = [0] * len(vocabulary)
            vector[index[term]] = 1
            doc_vectors.append(vector)
        result.append(doc_vectors)
    return result


def tf_idf(tokenized_docs: list[list[str]], vocabulary: list[str], bow: list[list[int]]) -> list[list[float]]:
    n_docs = len(tokenized_docs)
    doc_freq = [0] * len(vocabulary)
    for j in range(len(vocabulary)):
        doc_freq[j] = sum(1 for row in bow if row[j] > 0)

    idf = [math.log((n_docs + 1) / (doc_freq[j] + 1)) + 1 for j in range(len(vocabulary))]

    matrix = []
    for row in bow:
        tf_idf_row = [round(row[j] * idf[j], 4) for j in range(len(vocabulary))]
        matrix.append(tf_idf_row)
    return matrix


def vectorize(documents: list[str]) -> dict:
    tokenized_docs = _tokenize_documents(documents)
    vocabulary = build_vocabulary(tokenized_docs)
    bow = bag_of_words(tokenized_docs, vocabulary)
    oh = one_hot(tokenized_docs, vocabulary)
    tfidf = tf_idf(tokenized_docs, vocabulary, bow)
    return {
        "vocabulary": vocabulary,
        "one_hot": oh,
        "bag_of_words": bow,
        "tf_idf": tfidf,
    }
