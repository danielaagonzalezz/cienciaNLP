# cienciaNLP

[![tests](https://github.com/danielaagonzalezz/cienciaNLP/actions/workflows/tests.yml/badge.svg)](https://github.com/danielaagonzalezz/cienciaNLP/actions/workflows/tests.yml)
[![Documentación](https://readthedocs.org/projects/ciencianlp/badge/?version=latest)](https://ciencianlp.readthedocs.io/es/latest/)

Práctica de **Minería de Textos** (4º INF-A, CUNEF): clasificar textos en **esperanto** por temática científica
(**física**, **biología** y **química**).

El repositorio tiene tres partes:

1. **Dataset:** párrafos de la Wikipedia en esperanto, etiquetados por temática.
2. **Librería `ciencianlp`:** NLP para esperanto basado en reglas, construida desde cero (sin spaCy, NLTK ni Stanza),
   con una API parecida a la de spaCy.
3. **Cuaderno de Colab:** entrena y evalúa un clasificador y lo prueba con una página web real. *(en desarrollo)*

## Estado

| Parte | Estado |
|---|---|
| Repositorio, licencia y tests automáticos | Hecho |
| Script del dataset y dataset | Hecho |
| Librería: tokenizador, `Token`/`Doc`, stop-words, etiquetador POS, lematizador | Hecho |
| Librería: objeto `nlp` y exportación en `__init__.py` | Pendiente |
| Documentación en Read the Docs | Montada, se completa con la librería |
| Cuaderno de clasificación (fase 3) | Pendiente |

## Instalación

```
pip install git+https://github.com/danielaagonzalezz/cienciaNLP.git
```

## Uso

```python
from ciencianlp.doc import Doc

doc = Doc("Mi vidas la grandajn hundojn kaj H2O.")
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

Cada `Token` tiene `text`, `idx` (posición en el texto), `lemma_`, `pos_` (etiqueta de Universal Dependencies),
`is_stop`, `is_alpha`, `is_digit` e `is_punct`. Un `Doc` se recorre con `for`, admite `len()` y `doc[i]`.

La referencia completa de la API está en https://ciencianlp.readthedocs.io/es/latest/.

## Cómo funciona la librería

El esperanto es muy regular, así que la mayoría de las reglas salen de su gramática:

| Módulo | Qué hace |
|---|---|
| `tokenizer.py` | Divide el texto en palabras y signos. Mantiene juntas las letras ĉ, ĝ, ĥ, ĵ, ŝ, ŭ y las fórmulas como `H2O`. |
| `stopwords.py` | Genera las palabras vacías (artículo, pronombres, preposiciones, correlativos...) a partir de la gramática. |
| `pos.py` | Etiqueta cada palabra: primero las de clase cerrada y luego, por la terminación, `-o` sustantivo, `-a` adjetivo, `-e` adverbio, `-as/-is/-os/-us/-u/-i` verbo. |
| `lemma.py` | Devuelve la forma base: quita el plural `-j`, el acusativo `-n` y la terminación del verbo (`hundojn` → `hundo`, `iras` → `iri`). |
| `doc.py` | Las clases `Token` y `Doc`, que unen todo lo anterior. |

Limitaciones: el etiquetador no mira el contexto, etiqueta cada palabra por separado, y los nombres propios o las siglas
pueden quedar como `X`.

## Dataset

Está en [`dataset/dataset.csv`](dataset/dataset.csv): `UTF-8`, separador `;`, columnas `text;class`, un párrafo por fila.

| Clase | Categoría de Wikipedia | Párrafos |
|---|---|---|
| `fiziko` (física) | `Kategorio:Fiziko` | 375 |
| `biologio` (biología) | `Kategorio:Biologio` | 391 |
| `kemio` (química) | `Kategorio:Kemio` | 357 |

Cómo se construyó:

1. [`scripts/build_dataset.py`](scripts/build_dataset.py) recorre cada categoría y sus subcategorías, lee los artículos con
   `WikiPage.look_up` (de la biblioteca [esperantilo](https://github.com/jparisu/nlp-esperantilo)) y se queda con los
   párrafos de al menos 30 palabras, con un máximo de 5 por artículo. Espera entre peticiones, reintenta si falla la red
   y guarda una copia de cada clase por si se interrumpe.
2. [`scripts/clean_dataset.py`](scripts/clean_dataset.py) quita los párrafos repetidos, los que aparecen en dos clases a
   la vez, y los que conservan restos de fórmulas LaTeX, enlaces o referencias.

Para regenerarlo (tarda unos 45 minutos por los tiempos de espera con Wikipedia):

```
pip install requests git+https://github.com/jparisu/nlp-esperantilo.git
python scripts/build_dataset.py
python scripts/clean_dataset.py
```

**Ruido conocido.** Cada párrafo hereda la etiqueta del artículo del que sale, y no todos hablan del tema. Por ejemplo,
hay un párrafo sobre barreras acústicas en `fiziko`. Los textos que aparecían en dos clases se eliminaron, 40 filas. La
medición del ruido se hará en el cuaderno.

## Estructura del repositorio

```
cienciaNLP/
├── src/ciencianlp/     # la librería
├── tests/              # tests con pytest
├── scripts/            # build_dataset.py y clean_dataset.py
├── dataset/            # dataset.csv
├── docs/               # documentación (MkDocs)
└── .github/workflows/  # tests automáticos en cada push
```

## Tests

```
pip install -e ".[test]"
python -m pytest
```

GitHub Actions los ejecuta en cada `push` y `pull request`.

## Equipo

- Daniela González — [@danielaagonzalezz](https://github.com/danielaagonzalezz)
- Olivia — [@Olivia029](https://github.com/Olivia029)
- *(tercer miembro)*

Cada uno trabaja en su propia rama y entra en `main` con un pull request.

## Licencia y atribución

El código tiene licencia [MIT](LICENSE). Los textos del dataset proceden de la Wikipedia en esperanto y se distribuyen con
su licencia, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
