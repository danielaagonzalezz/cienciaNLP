from ciencianlp.tokenizer import tokenize


def textos(frase):
    return [t for t, _ in tokenize(frase)]


def test_frase_simple():
    assert textos("La akvo bolas.") == ["La", "akvo", "bolas", "."]


def test_letras_del_esperanto():
    assert textos("ĉirkaŭ ĝi ŝi") == ["ĉirkaŭ", "ĝi", "ŝi"]


def test_guion_y_apostrofo_aparte():
    assert textos("ĉi-tie") == ["ĉi", "-", "tie"]


def test_formulas_y_numeros():
    assert textos("H2O y 3,14.") == ["H2O", "y", "3,14", "."]


def test_ordinales_con_cifras_juntos():
    assert textos("la 1987-a jaro") == ["la", "1987-a", "jaro"]
    assert textos("la 20-an de majo") == ["la", "20-an", "de", "majo"]
    assert textos("paĝoj 12-15") == ["paĝoj", "12", "-", "15"]  # un rango no es un ordinal


def test_posiciones():
    texto = "La  akvo"
    for token, pos in tokenize(texto):
        assert texto[pos:pos + len(token)] == token


def test_vacio():
    assert tokenize("") == []