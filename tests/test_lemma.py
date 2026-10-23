from ciencianlp.doc import Doc
from ciencianlp.lemma import lematizar


def test_sustantivos():
    for palabra in ["hundo", "hundoj", "hundon", "hundojn", "Hundo"]:
        assert lematizar(palabra) == "hundo", palabra


def test_adjetivos():
    for palabra in ["granda", "grandaj", "grandan", "grandajn"]:
        assert lematizar(palabra) == "granda", palabra


def test_verbos_todas_las_terminaciones():
    for palabra in ["iras", "iris", "iros", "irus", "iru", "iri"]:
        assert lematizar(palabra) == "iri", palabra
    assert lematizar("estas") == "esti"
    assert lematizar("estis") == "esti"


def test_adverbios():
    assert lematizar("rapide") == "rapide"
    assert lematizar("hejmen") == "hejme"
    assert lematizar("supren") == "supre"


def test_adverbios_que_acaban_en_n_pero_no_son_acusativo():
    assert lematizar("tamen") == "tamen"
    assert lematizar("ajn") == "ajn"
    assert lematizar("Stephen") == "stephen"


def test_pronombres_y_determinantes():
    assert lematizar("min") == "mi"
    assert lematizar("ilin") == "ili"
    assert lematizar("miajn") == "mia"
    assert lematizar("kiujn") == "kiu"
    assert lematizar("kion") == "kio"


def test_palabras_que_no_cambian():
    for palabra in ["la", "kaj", "en", "kiam", "dudek", "kies"]:
        assert lematizar(palabra) == palabra, palabra


def test_puntuacion_numeros_y_desconocidos():
    assert lematizar(".") == "."
    assert lematizar("2020") == "2020"
    assert lematizar("H2O") == "h2o"
    assert lematizar("DNA") == "dna"


def test_los_lemas_coinciden_entre_formas():
    assert lematizar("hundoj") == lematizar("hundon") == lematizar("hundo")


def test_el_doc_rellena_lemma_():
    doc = Doc("La grandajn hundojn mi vidas.")
    assert [t.lemma_ for t in doc] == ["la", "granda", "hundo", "mi", "vidi", "."]