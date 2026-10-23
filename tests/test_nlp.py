from ciencianlp import Doc, Token, nlp


def test_nlp_devuelve_un_doc():
    doc = nlp("La akvo bolas.")
    assert isinstance(doc, Doc)
    assert len(doc) == 4


def test_nlp_rellena_lema_pos_y_stop():
    doc = nlp("Mi vidas la grandajn hundojn.")
    assert [t.lemma_ for t in doc] == ["mi", "vidi", "la", "granda", "hundo", "."]
    assert [t.pos_ for t in doc] == ["PRON", "VERB", "DET", "ADJ", "NOUN", "PUNCT"]
    assert [t.is_stop for t in doc] == [True, False, True, False, False, False]


def test_nlp_con_texto_vacio():
    assert len(nlp("")) == 0


def test_doc_y_token_se_pueden_importar_del_paquete():
    assert isinstance(nlp("akvo")[0], Token)