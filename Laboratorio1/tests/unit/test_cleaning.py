from core.cleaning import clean_text, clean_texts


def test_lowercase():
    assert clean_text("HOLA Mundo") == "hola mundo"


def test_removes_punctuation_without_concatenating():
    result = clean_text("perro,gato")
    assert "," not in result
    assert "perrogato" not in result


def test_removes_stopwords():
    result = clean_text("el perro y la casa")
    tokens = result.split()
    assert "el" not in tokens
    assert "la" not in tokens
    assert "y" not in tokens
    assert "perro" in tokens
    assert "casa" in tokens


def test_preserves_accents_enye_and_digits():
    result = clean_text("Año 2024 pequeño camión")
    assert "año" in result
    assert "2024" in result
    assert "pequeño" in result
    assert "camión" in result


def test_normalizes_whitespace():
    result = clean_text("   perro    gato   ")
    assert "  " not in result
    assert result == result.strip()


def test_clean_texts_batch_preserves_order():
    results = clean_texts(["Perro", "Gato", "Casa"])
    assert len(results) == 3
    assert "perro" in results[0]
    assert "gato" in results[1]
    assert "casa" in results[2]
