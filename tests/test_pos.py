from ciencianlp.doc import Doc
from ciencianlp.pos import etiquetar
from ciencianlp.stopwords import STOP_WORDS


def etiquetas(frase):
    return [t.pos_ for t in Doc(frase)]


def test_frase_simple():
    assert etiquetas("La akvo bolas.") == ["DET", "NOUN", "VERB", "PUNCT"]


def test_frase_con_acusativo_y_conjuncion():
    assert etiquetas("Mi vidas la grandan hundon kaj ĝi estas bela.") == [
        "PRON", "VERB", "DET", "ADJ", "NOUN", "CCONJ", "PRON", "VERB", "ADJ", "PUNCT"]


def test_sustantivos_con_plural_y_acusativo():
    for palabra in ["hundo", "hundoj", "hundon", "hundojn", "Eŭropo"]:
        assert etiquetar(palabra) == "NOUN", palabra


def test_adjetivos_con_plural_y_acusativo():
    for palabra in ["granda", "grandaj", "grandan", "grandajn"]:
        assert etiquetar(palabra) == "ADJ", palabra


def test_adverbios():
    for palabra in ["rapide", "bone", "hejmen"]:
        assert etiquetar(palabra) == "ADV", palabra


def test_formas_verbales():
    for palabra in ["iras", "iris", "iros", "irus", "iru", "iri", "estas"]:
        assert etiquetar(palabra) == "VERB", palabra


def test_clase_cerrada_gana_a_la_terminacion():
    # Acaban en -o, -a, -e o -u pero no son sustantivo, adjetivo, adverbio ni verbo.
    assert etiquetar("kio") == "PRON"
    assert etiquetar("kiu") == "PRON"
    assert etiquetar("kia") == "DET"
    assert etiquetar("kie") == "ADV"
    assert etiquetar("ĉe") == "ADP"
    assert etiquetar("ke") == "SCONJ"
    assert etiquetar("mi") == "PRON"


def test_pronombres_y_posesivos_declinados():
    assert etiquetar("ĝin") == "PRON"
    assert etiquetar("ilin") == "PRON"
    assert etiquetar("mia") == "DET"
    assert etiquetar("miajn") == "DET"


def test_correlativos_declinados():
    assert etiquetar("kiujn") == "PRON"
    assert etiquetar("kion") == "PRON"
    assert etiquetar("tiajn") == "DET"
    assert etiquetar("kies") == "DET"
    assert etiquetar("neniam") == "ADV"


def test_conjunciones():
    assert etiquetar("kaj") == "CCONJ"
    assert etiquetar("sed") == "CCONJ"
    assert etiquetar("ĉar") == "SCONJ"
    assert etiquetar("se") == "SCONJ"


def test_numeros():
    for palabra in ["tri", "dudek", "tricent", "mil", "2020", "3,14"]:
        assert etiquetar(palabra) == "NUM", palabra


def test_puntuacion():
    for simbolo in [",", ".", "(", "«", "-"]:
        assert etiquetar(simbolo) == "PUNCT", simbolo


def test_desconocido():
    for palabra in ["H2O", "Einstein", "DNA"]:
        assert etiquetar(palabra) == "X", palabra


def test_no_distingue_mayusculas():
    assert etiquetar("La") == "DET"
    assert etiquetar("KAJ") == "CCONJ"


def test_raices_cortas_no_son_verbos():
    # "gas" no es una forma verbal: la raíz sería de una sola letra.
    assert etiquetar("gas") == "X"


def test_toda_stop_word_tiene_etiqueta():
    sin_etiqueta = [w for w in STOP_WORDS if etiquetar(w) == "X"]
    assert sin_etiqueta == []
