# ciencianlp

Librería de NLP **basada en reglas** para esperanto, construida desde cero (sin spaCy, NLTK ni Stanza) con una API similar a la de spaCy. Forma parte de la práctica de Minería de Textos:
clasificar textos en esperanto por temática científica (física, biología y química).

El esperanto es muy regular: sus palabras se forman con raíces y terminaciones fijas. Por eso las reglas de la librería salen casi directamente de su gramática, sin diccionarios ni modelos entrenados.

## Instalación

```
pip install git+https://github.com/danielaagonzalezz/cienciaNLP.git
```

En un cuaderno de Jupyter o de Google Colab:

```
!pip install git+https://github.com/danielaagonzalezz/cienciaNLP.git
```

La librería no tiene dependencias.

## Uso

`nlp(texto)` devuelve un `Doc`, que se recorre token a token:

```python
from ciencianlp import nlp

doc = nlp("Mi vidas la grandajn hundojn kaj H2O.")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.is_stop)
```

```
Mi mi PRON True
vidas vidi VERB False
la la DET True
grandajn granda ADJ False
hundojn hundo NOUN False
kaj kaj CCONJ True
H2O h2o X False
. . PUNCT False
```

Un `Doc` admite `len(doc)` (aquí, 8 tokens) y acceso por posición (`doc[1]` es `vidas`).
También se puede crear directamente con `from ciencianlp.doc import Doc`.

### Atributos de `Token`

| Atributo | Qué contiene |
|---|---|
| `text` | El texto del token, tal como aparece |
| `idx` | Posición del token en el texto original |
| `lemma_` | Forma base (`hundojn` → `hundo`, `vidas` → `vidi`) |
| `pos_` | Categoría gramatical, con las etiquetas de Universal Dependencies |
| `is_stop` | `True` si es una palabra vacía (`la`, `kaj`, `de`...) |
| `is_alpha` | `True` si son solo letras |
| `is_digit` | `True` si son solo dígitos |
| `is_punct` | `True` si es un signo de puntuación |

## Cómo funciona

| Módulo | Qué hace |
|---|---|
| `tokenizer.py` | Divide el texto en palabras y signos. Mantiene juntas las letras ĉ, ĝ, ĥ, ĵ, ŝ, ŭ y las fórmulas como `H2O`. |
| `stopwords.py` | Genera las palabras vacías (artículo, pronombres, preposiciones, correlativos...) a partir de la gramática. |
| `pos.py` | Etiqueta cada palabra: primero las de clase cerrada y luego, por la terminación, `-o` sustantivo, `-a` adjetivo, `-e` adverbio, `-as/-is/-os/-us/-u/-i` verbo. |
| `lemma.py` | Devuelve la forma base: quita el plural `-j`, el acusativo `-n` y la terminación del verbo (`hundojn` → `hundo`, `iras` → `iri`). |
| `doc.py` | Las clases `Token` y `Doc`, que unen todo lo anterior. |

!!! note "Limitaciones"
    El etiquetador no mira el contexto: etiqueta cada palabra por separado. Los nombres propios y las siglas pueden quedar como `X`.

## Referencia de la API

La [referencia de la API](api.md) se genera sola a partir de los *docstrings* del código.

## Más información

- [Repositorio en GitHub](https://github.com/danielaagonzalezz/cienciaNLP): código, tests, dataset y README.
- [Cuaderno de clasificación](https://github.com/danielaagonzalezz/cienciaNLP/blob/main/notebooks/clasificacion_esperanto.ipynb):
  usa la librería para entrenar un clasificador de textos y probarlo con páginas web reales.

## Licencia

El código tiene licencia MIT. Los textos del dataset proceden de la Wikipedia en esperanto (licencia CC BY-SA 4.0).
