from ciencianlp.doc import Doc


def test_doc_se_recorre_como_en_spacy():
    doc = Doc("La akvo bolas.")
    assert [t.text for t in doc] == ["La", "akvo", "bolas", "."]
    assert len(doc) == 4
    assert doc[1].text == "akvo"


def test_idx_es_la_posicion_en_el_texto():
    doc = Doc("La akvo")
    assert [t.idx for t in doc] == [0, 3]


def test_is_alpha_is_digit_is_punct():
    doc = Doc("akvo 2020 H2O .")
    akvo, anyo, formula, punto = doc
    assert akvo.is_alpha and not akvo.is_digit and not akvo.is_punct
    assert anyo.is_digit and not anyo.is_alpha
    assert not formula.is_alpha and not formula.is_punct
    assert punto.is_punct


def test_valores_provisionales():
    token = Doc("Akvo")[0]
    assert token.lemma_ == "akvo"
    assert token.pos_ == "NOUN"
    assert token.is_stop is False

def test_is_stop_se_marca_al_crear_el_doc():
    doc = Doc("La akvo bolas kaj ĝi estas varma.")
    assert [t.is_stop for t in doc] == [True, False, False, True, True, True, False, False]