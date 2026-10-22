"""Stop-words del esperanto, construidas a partir de su gramática.

Las stop-words son palabras gramaticales de clase cerrada (artículo, pronombres,
preposiciones, conjunciones, correlativos...). En esperanto la mayoría se pueden
generar con reglas, así que no hace falta escribirlas una a una:

* Los correlativos (kiu, tio, ie, ĉiam, nenial...) son prefijo + sufijo.
* Los pronombres admiten acusativo (-n) y forman posesivos (-a, -aj, -an, -ajn).
* Los correlativos en -u y -a admiten plural y acusativo (-j, -n, -jn); los
  correlativos en -o solo acusativo (-n).
"""

# Artículo (el esperanto solo tiene uno, invariable).
ARTICULO = {"la"}

# Pronombres personales y reflexivos (sin declinar).
PRONOMBRES = {"mi", "vi", "li", "ŝi", "ĝi", "ni", "ili", "oni", "si", "ci"}

PREPOSICIONES = {
    "al", "anstataŭ", "antaŭ", "apud", "ĉe", "ĉirkaŭ", "da", "de", "dum", "ekde",
    "ekster", "el", "en", "inter", "je", "kontraŭ", "krom", "kun", "laŭ", "malgraŭ",
    "minus", "per", "plus", "po", "por", "post", "preter", "pri", "pro", "sen",
    "sub", "super", "sur", "tra", "trans", "ĝis",
}

CONJUNCIONES = {
    "kaj", "aŭ", "nek", "sed", "ĉar", "ke", "se", "ol", "do", "tamen", "kvankam", "kvazaŭ",
}

# Adverbios y partículas de uso muy frecuente.
PARTICULAS_Y_ADVERBIOS = {
    "ne", "jes", "jen", "ja", "ĉu", "ju", "des", "ajn", "nur", "eĉ", "ankaŭ", "ankoraŭ",
    "jam", "tre", "tro", "pli", "plej", "for", "tuj", "baldaŭ", "almenaŭ", "apenaŭ",
    "mem", "ĉi",
}

# Numerales cardinales básicos.
NUMERALES = {
    "unu", "du", "tri", "kvar", "kvin", "ses", "sep", "ok", "naŭ", "dek", "cent", "mil",
    "nul",
}

# Formas del verbo "esti" (cópula).
VERBO_ESTI = {"esti", "estas", "estis", "estos", "estus", "estu", "estante", "estinte"}

# Tabla de correlativos: prefijo + sufijo.
PREFIJOS_CORRELATIVOS = ("ki", "ti", "i", "ĉi", "neni")
SUFIJOS_CORRELATIVOS = ("u", "o", "a", "e", "el", "es", "al", "am", "om")


def _correlativos() -> set:
    """Los 45 correlativos (kiu, kio, kia, kie, kiel... nenial, neniam, neniom)."""
    return {p + s for p in PREFIJOS_CORRELATIVOS for s in SUFIJOS_CORRELATIVOS}


def _con_flexion(base: set, terminaciones: tuple) -> set:
    """Cada palabra de ``base`` seguida de cada una de las ``terminaciones``."""
    return {palabra + fin for palabra in base for fin in terminaciones}


def _construir() -> frozenset:
    correlativos = _correlativos()
    terminan_en_u_o_a = {w for w in correlativos if w.endswith(("u", "a"))}
    terminan_en_o = {w for w in correlativos if w.endswith("o")}
    resto = correlativos - terminan_en_u_o_a - terminan_en_o

    posesivos = {p + "a" for p in PRONOMBRES - {"oni"}}  # mia, via, lia, ŝia, ĝia, nia, ilia, sia, cia

    palabras = set()
    palabras |= ARTICULO | PREPOSICIONES | CONJUNCIONES | PARTICULAS_Y_ADVERBIOS
    palabras |= NUMERALES | VERBO_ESTI
    palabras |= _con_flexion(PRONOMBRES, ("", "n"))              # mi, min
    palabras |= _con_flexion(posesivos, ("", "j", "n", "jn"))    # mia, miaj, mian, miajn
    palabras |= _con_flexion(terminan_en_u_o_a, ("", "j", "n", "jn"))  # kiu, kiuj, kiun, kiujn
    palabras |= _con_flexion(terminan_en_o, ("", "n"))           # kio, kion
    palabras |= resto                                            # kie, kiel, kiam...
    return frozenset(palabras)


STOP_WORDS = _construir()


def es_stop_word(palabra: str) -> bool:
    """``True`` si la palabra es una stop-word (no distingue mayúsculas)."""
    return palabra.lower() in STOP_WORDS
