from ciencianlp.stopwords import STOP_WORDS, es_stop_word


def test_palabras_gramaticales_son_stop_words():
    for palabra in ["la", "kaj", "de", "en", "ne", "ankaŭ", "estas", "mi"]:
        assert es_stop_word(palabra), palabra


def test_palabras_de_contenido_no_son_stop_words():
    for palabra in ["akvo", "fiziko", "kemio", "biologio", "bolas", "varma"]:
        assert not es_stop_word(palabra), palabra


def test_no_distingue_mayusculas():
    assert es_stop_word("La")
    assert es_stop_word("KAJ")
    assert not es_stop_word("Akvo")


def test_correlativos_generados_por_regla():
    # La tabla completa son 5 prefijos x 9 sufijos = 45 palabras.
    for palabra in ["kiu", "kio", "kia", "kie", "kiel", "kies", "kial", "kiam", "kiom",
                    "tiu", "iu", "ĉiu", "neniu", "ĉiam", "neniam", "tial", "ĉie"]:
        assert es_stop_word(palabra), palabra


def test_correlativos_con_plural_y_acusativo():
    for palabra in ["kiuj", "kiun", "kiujn", "tiuj", "ĉiujn", "neniuj", "kian", "tiajn", "kion"]:
        assert es_stop_word(palabra), palabra


def test_correlativos_no_aceptan_terminaciones_imposibles():
    # -o no tiene plural; los adverbios (-e, -el, -am...) no se declinan.
    for palabra in ["kioj", "kiojn", "kien", "kiamj"]:
        assert not es_stop_word(palabra), palabra


def test_pronombres_y_posesivos_declinados():
    for palabra in ["min", "vin", "lin", "ilin", "mia", "miaj", "mian", "viajn", "ŝiaj", "ilia"]:
        assert es_stop_word(palabra), palabra


def test_formas_de_esti():
    for palabra in ["esti", "estas", "estis", "estos", "estus", "estu"]:
        assert es_stop_word(palabra), palabra


def test_numerales_basicos():
    for palabra in ["unu", "du", "tri", "dek", "cent", "mil"]:
        assert es_stop_word(palabra), palabra


def test_la_lista_es_inmutable_y_no_vacia():
    assert isinstance(STOP_WORDS, frozenset)
    assert len(STOP_WORDS) > 200
