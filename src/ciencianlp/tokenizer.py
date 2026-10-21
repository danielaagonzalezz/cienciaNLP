"""Tokenizador de esperanto basado en reglas."""

import re

PATRON = re.compile(
    r"\d+(?:[.,]\d+)+"  # número con decimales: 3,14
    r"|[^\W_]+"         # palabra o fórmula: akvo, ĉirkaŭ, H2O
    r"|\S"              # cualquier otro símbolo suelto: , . ( ) -
)


def tokenize(texto):
    """Divide un texto en tokens. Devuelve una lista de pares (token, posición)."""
    return [(m.group(), m.start()) for m in PATRON.finditer(texto)]