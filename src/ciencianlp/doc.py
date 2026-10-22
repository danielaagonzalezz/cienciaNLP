"""Objetos Token y Doc, con una API parecida a la de spaCy."""

from ciencianlp.pos import etiquetar
from ciencianlp.stopwords import es_stop_word
from ciencianlp.tokenizer import tokenize

class Token:
    """Una palabra o un signo de un texto."""

    def __init__(self, text, idx):
        self.text = text
        self.idx = idx  # posición en el texto original
        self.is_stop = es_stop_word(text)
        self.pos_ = etiquetar(text)
        # Provisional: lo cambiará en el lematizador 
        self.lemma_ = text.lower()
        

    @property  # se usa sin paréntesis: token.is_alpha
    def is_alpha(self):
        return self.text.isalpha()

    @property
    def is_digit(self):
        return self.text.isdigit()

    @property
    def is_punct(self):
        # puntuación = no tiene ninguna letra ni número
        return not any(c.isalnum() for c in self.text)

    def __repr__(self):
        return self.text


class Doc:
    """Un texto ya dividido en tokens.

    Examples:
        >>> doc = Doc("La akvo bolas.")
        >>> [token.text for token in doc]
        ['La', 'akvo', 'bolas', '.']
    """

    def __init__(self, text):
        self.text = text
        self.tokens = [Token(t, i) for t, i in tokenize(text)]

    def __iter__(self):  # for token in doc
        return iter(self.tokens)

    def __len__(self):  # len(doc)
        return len(self.tokens)

    def __getitem__(self, i):  # doc[1]
        return self.tokens[i]

    def __repr__(self):
        return self.text