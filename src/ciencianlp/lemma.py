"""Lematizador del esperanto basado en reglas.

El lema es la forma base de una palabra: el sustantivo acaba en -o, el adjetivo en -a,
el adverbio en -e y el verbo en -i. Para llegar a ella se quitan el plural (-j), el
acusativo (-n) y la terminación del verbo. El lema sale siempre en minúsculas.
"""

from typing import Optional

from ciencianlp.pos import (
    NOMBRE_O_ADJETIVO,
    RAIZ_MINIMA,
    TABLA,
    TERMINACIONES_VERBALES,
    etiquetar,
)
from ciencianlp.stopwords import VERBO_ESTI


def lematizar(palabra: str, pos: Optional[str] = None) -> str:
    """Devuelve el lema de una palabra.

    Args:
        palabra: La palabra tal como aparece en el texto.
        pos: Su etiqueta gramatical. Si no se da, se calcula con ``etiquetar``.

    Returns:
        El lema, en minúsculas.

    Examples:
        >>> lematizar("hundojn")
        'hundo'
        >>> lematizar("grandajn")
        'granda'
        >>> lematizar("kuras")
        'kuri'
    """
    w = palabra.lower()
    pos = pos or etiquetar(w)

    if pos in ("NOUN", "ADJ"):
        m = NOMBRE_O_ADJETIVO.fullmatch(w)
        return m.group(1) + m.group(2)  # hundojn -> hund + o
    if pos == "VERB":
        if w in VERBO_ESTI:
            return "esti"
        for fin in TERMINACIONES_VERBALES:
            if w.endswith(fin) and len(w) - len(fin) >= RAIZ_MINIMA:
                return w[: -len(fin)] + "i"  # iras -> ir + i
    if pos in ("PRON", "DET") and w.endswith("n") and len(w) > RAIZ_MINIMA:
        w = w[:-1]  # min -> mi
    if pos == "ADV" and w.endswith("en") and w not in TABLA and palabra.islower():
        w = w[:-1]  # rapiden -> rapide (pero tamen y ajn no llevan acusativo, ni los nombres propios)
    if pos in ("PRON", "DET") and w.endswith("j") and len(w) > RAIZ_MINIMA:
        w = w[:-1]  # kiuj -> kiu
    return w