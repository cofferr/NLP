from core.vectorize import vectorize

# Caso verificado a mano:
# docs limpios -> tokens: doc0=["gato"], doc1=["perro", "gato"]
# vocabulario lexicográfico: ["gato", "perro"]
# bag_of_words: doc0=[1,0], doc1=[1,1]
# doc_freq: gato=2 (aparece en ambos), perro=1 (aparece en 1)
# idf(t) = ln((|D|+1)/(n_t+1)) + 1, |D|=2
#   idf(gato) = ln(3/3)+1 = 1.0
#   idf(perro) = ln(3/2)+1 = 1.4055 (redondeado a 4 decimales)
# tf_idf: doc0 = [1*1.0, 0*1.4055] = [1.0, 0.0]
#         doc1 = [1*1.0, 1*1.4055] = [1.0, 1.4055]


def test_vocabulary_is_sorted_lexicographically():
    result = vectorize(["gato", "perro gato"])
    assert result["vocabulary"] == ["gato", "perro"]


def test_bag_of_words_counts_and_order():
    result = vectorize(["gato", "perro gato"])
    assert result["bag_of_words"] == [[1, 0], [1, 1]]


def test_one_hot_per_occurrence():
    result = vectorize(["gato", "perro gato"])
    # doc0 tiene una ocurrencia: "gato" -> [1, 0]
    assert result["one_hot"][0] == [[1, 0]]
    # doc1 tiene dos ocurrencias en orden: "perro" -> [0,1], "gato" -> [1,0]
    assert result["one_hot"][1] == [[0, 1], [1, 0]]


def test_tf_idf_matches_manual_calculation():
    result = vectorize(["gato", "perro gato"])
    assert result["tf_idf"] == [[1.0, 0.0], [1.0, 1.4055]]


def test_tf_idf_repeated_term_uses_absolute_frequency():
    # doc0="gato perro", doc1="perro perro gato" -> ambos términos en ambos docs (n_t=2)
    result = vectorize(["gato perro", "perro perro gato"])
    # idf = ln(3/3)+1 = 1.0 para ambos términos
    assert result["vocabulary"] == ["gato", "perro"]
    assert result["bag_of_words"] == [[1, 1], [1, 2]]
    assert result["tf_idf"] == [[1.0, 1.0], [1.0, 2.0]]


def test_vectorize_preserves_document_order():
    result = vectorize(["perro", "gato", "casa"])
    assert len(result["bag_of_words"]) == 3
    assert len(result["one_hot"]) == 3
    assert len(result["tf_idf"]) == 3
