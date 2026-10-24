"""ciencianlp: librería de NLP basada en reglas para esperanto."""

__version__ = "0.1.0"

from ciencianlp.doc import Doc, Token

__all__ = ["Doc", "Token", "nlp"]

def nlp(texto):
    """Procesa un texto y devuelve un ``Doc``, como ``nlp("texto")`` en spaCy.

    El ``Doc`` ya trae, para cada token, su lema (``lemma_``), su etiqueta
    gramatical (``pos_``) y si es una stop-word (``is_stop``).

    Examples:
        >>> from ciencianlp import nlp
        >>> doc = nlp("La akvo bolas.")
        >>> [(t.text, t.pos_) for t in doc]
        [('La', 'DET'), ('akvo', 'NOUN'), ('bolas', 'VERB'), ('.', 'PUNCT')]
    """
    return Doc(texto)