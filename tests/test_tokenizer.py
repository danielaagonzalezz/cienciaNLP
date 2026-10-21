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


def test_posiciones():
    texto = "La  akvo"
    for token, pos in tokenize(texto):
        assert texto[pos:pos + len(token)] == token


def test_vacio():
    assert tokenize("") == []