"""Etiquetador gramatical (POS-tagging) del esperanto basado en reglas.

Etiquetas (las de Universal Dependencies, como spaCy):
NOUN, ADJ, ADV, VERB, PRON, DET, ADP, CCONJ, SCONJ, NUM, PUNCT y X (desconocido).

En esperanto la categoría de casi todas las palabras se deduce de su terminación,
así que el etiquetador sigue este orden:

1. Puntuación y números.
2. Palabras de clase cerrada (artículo, pronombres, preposiciones, conjunciones,
   correlativos, numerales...). Se miran antes que las terminaciones, porque no
   siguen la regla: ``kio`` acaba en -o y no es un sustantivo.
3. Clase abierta, por la terminación:

   ======================  ==========  ===========================
   terminación             etiqueta    ejemplos
   ======================  ==========  ===========================
   -o (-oj, -on, -ojn)     NOUN        hundo, hundojn
   -a (-aj, -an, -ajn)     ADJ         granda, grandajn
   -e (y -en)              ADV         rapide, hejmen
   -as -is -os -us -u -i   VERB        iras, iris, iros, irus, iru, iri
   ======================  ==========  ===========================

4. Cualquier otra cosa (fórmulas, siglas en mayúsculas, nombres propios sin
   terminación...) es ``X``.

El etiquetador no mira el contexto: etiqueta cada palabra por separado.
"""
import re

from ciencianlp.stopwords import (
    NUMERALES,
    PARTICULAS_Y_ADVERBIOS,
    PREFIJOS_CORRELATIVOS,
    PREPOSICIONES,
    PRONOMBRES,
    SUFIJOS_CORRELATIVOS,
    VERBO_ESTI,
)

# Conjunciones: las coordinantes unen elementos equivalentes; las subordinantes
# introducen una oración dependiente. "ĉu" se trata como subordinante ("si").
COORDINANTES = {"kaj", "aŭ", "nek", "sed", "do"}
SUBORDINANTES = {"ĉar", "ke", "se", "ol", "kvankam", "kvazaŭ", "ĉu"}
ADVERBIOS_EXTRA = {"tamen"}

# Numerales compuestos: dudek, tricent, mil, kvarmil...
NUMERAL_COMPUESTO = re.compile(r"(?:(?:unu|du|tri|kvar|kvin|ses|sep|ok|naŭ)?(?:dek|cent|mil))+")
NUMERO = re.compile(r"\d+(?:[.,]\d+)*")

# Sustantivos y adjetivos: base en -o / -a con plural (-j) y acusativo (-n) opcionales.
NOMBRE_O_ADJETIVO = re.compile(r"(.+)([ao])j?n?")
ADVERBIO_ACUSATIVO = re.compile(r".+en")
TERMINACIONES_VERBALES = ("as", "is", "os", "us", "u", "i")
RAIZ_MINIMA = 2  # letras mínimas antes de la terminación (evita falsos verbos como "gas")


def _construir_tabla() -> dict:
    """Etiqueta de cada palabra de clase cerrada, incluidas sus formas declinadas."""
    tabla = {"la": "DET"}

    def anadir(palabras, etiqueta, terminaciones=("",)):
        for palabra in palabras:
            for fin in terminaciones:
                tabla[palabra + fin] = etiqueta

    anadir(PREPOSICIONES, "ADP")
    anadir(COORDINANTES, "CCONJ")
    anadir(SUBORDINANTES, "SCONJ")
    anadir(PARTICULAS_Y_ADVERBIOS | ADVERBIOS_EXTRA, "ADV")
    anadir(NUMERALES, "NUM")
    anadir(VERBO_ESTI, "VERB")

    anadir(PRONOMBRES, "PRON", ("", "n"))                         # mi, min
    anadir({p + "a" for p in PRONOMBRES - {"oni"}}, "DET",
           ("", "j", "n", "jn"))                                   # mia, miaj, mian, miajn

    # Correlativos: kiu/kio son pronombres, kia/kies determinantes, el resto adverbios.
    for prefijo in PREFIJOS_CORRELATIVOS:
        anadir({prefijo + "u"}, "PRON", ("", "j", "n", "jn"))      # kiu, kiuj, kiun, kiujn
        anadir({prefijo + "o"}, "PRON", ("", "n"))                 # kio, kion
        anadir({prefijo + "a"}, "DET", ("", "j", "n", "jn"))       # kia, kiaj...
        anadir({prefijo + "es"}, "DET")                            # kies
        for sufijo in SUFIJOS_CORRELATIVOS:
            if sufijo not in ("u", "o", "a", "es"):
                tabla[prefijo + sufijo] = "ADV"                    # kie, kiel, kiam...
    return tabla


TABLA = _construir_tabla()


def etiquetar(palabra: str) -> str:
    """Devuelve la etiqueta gramatical de una palabra (no distingue mayúsculas)."""
    w = palabra.lower()
    if not w:
        return "X"
    if not any(c.isalnum() for c in w):
        return "PUNCT"
    if NUMERO.fullmatch(w):
        return "NUM"
    if w in TABLA:
        return TABLA[w]
    if NUMERAL_COMPUESTO.fullmatch(w):
        return "NUM"
    if not w.isalpha():
        return "X"  # fórmulas y mezclas de letras y números: H2O
    if len(palabra) > 1 and palabra.isupper():
        return "X"  # siglas: DNA, NASA (acaban en vocal pero no son esperanto)

    m =NOMBRE_O_ADJETIVO.fullmatch(w)
    if m and len(m.group(1)) >= RAIZ_MINIMA:
        return "NOUN" if m.group(2) == "o" else "ADJ"
    if ADVERBIO_ACUSATIVO.fullmatch(w) and len(w) > RAIZ_MINIMA + 2:
        return "ADV"
    if w.endswith("e") and len(w) > RAIZ_MINIMA:
        return "ADV"
    for fin in TERMINACIONES_VERBALES:
        if w.endswith(fin) and len(w) - len(fin) >= RAIZ_MINIMA:
            return "VERB"
    return "X"
