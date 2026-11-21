# cienciaNLP

[![tests](https://github.com/danielaagonzalezz/cienciaNLP/actions/workflows/tests.yml/badge.svg)](https://github.com/danielaagonzalezz/cienciaNLP/actions/workflows/tests.yml)
[![Documentación](https://readthedocs.org/projects/ciencianlp/badge/?version=latest)](https://ciencianlp.readthedocs.io/es/latest/)

Práctica de **Minería de Textos** (4º INF-A, CUNEF): clasificar textos en **esperanto** por temática científica
(**física**, **biología** y **química**).

El repositorio tiene tres partes:

1. **Dataset:** párrafos de la Wikipedia en esperanto, etiquetados por temática.
2. **Librería `ciencianlp`:** NLP para esperanto basado en reglas, construida desde cero (sin spaCy, NLTK ni Stanza),
   con una API parecida a la de spaCy.
3. **Cuaderno de Colab** ([`notebooks/clasificacion_esperanto.ipynb`](notebooks/clasificacion_esperanto.ipynb)):
   entrena y evalúa un clasificador y lo prueba con páginas web reales.

## Estado

| Parte | Estado |
|---|---|
| Repositorio, licencia y tests automáticos | Hecho |
| Script del dataset y dataset | Hecho |
| Librería: tokenizador, `Token`/`Doc`, stop-words, etiquetador POS, lematizador | Hecho |
| Librería: objeto `nlp` y exportación en `__init__.py` | Hecho |
| Documentación en Read the Docs | Hecho |
| Cuaderno de clasificación (fase 3) | Hecho |

## Instalación

```
pip install git+https://github.com/danielaagonzalezz/cienciaNLP.git
```

## Uso

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

Cada `Token` tiene `text`, `idx` (posición en el texto), `lemma_`, `pos_` (etiqueta de Universal Dependencies),
`is_stop`, `is_alpha`, `is_digit` e `is_punct`. Un `Doc` se recorre con `for`, admite `len()` y `doc[i]`.
También se puede crear un `Doc` directamente con `from ciencianlp.doc import Doc`.
La referencia completa de la API está en https://ciencianlp.readthedocs.io/es/latest/.

## Cómo funciona la librería

El esperanto es muy regular, así que la mayoría de las reglas salen de su gramática:

| Módulo | Qué hace |
|---|---|
| `tokenizer.py` | Divide el texto en palabras y signos. Mantiene juntas las letras ĉ, ĝ, ĥ, ĵ, ŝ, ŭ y las fórmulas como `H2O`. |
| `stopwords.py` | Genera las palabras vacías (artículo, pronombres, preposiciones, correlativos...) a partir de la gramática. |
| `pos.py` | Etiqueta cada palabra: primero las de clase cerrada y luego, por la terminación, `-o` sustantivo, `-a` adjetivo, `-e` adverbio, `-as/-is/-os/-us/-u/-i` verbo. Los ordinales con cifras (`1987-a`, `20-an`) son adjetivos, como en Universal Dependencies. |
| `lemma.py` | Devuelve la forma base: quita el plural `-j`, el acusativo `-n` y la terminación del verbo (`hundojn` → `hundo`, `iras` → `iri`). |
| `doc.py` | Las clases `Token` y `Doc`, que unen todo lo anterior. |

Limitaciones: el etiquetador no mira el contexto, etiqueta cada palabra por separado, y los nombres propios o las siglas
pueden quedar como `X`.

## Dataset

Está en [`dataset/dataset.csv`](dataset/dataset.csv): `UTF-8`, separador `;`, columnas `text;class`, un párrafo por fila.

| Clase | Categoría de Wikipedia | Párrafos |
|---|---|---|
| `fiziko` (física) | `Kategorio:Fiziko` | 368 |
| `biologio` (biología) | `Kategorio:Biologio` | 372 |
| `kemio` (química) | `Kategorio:Kemio` | 358 |

Cómo se construyó:

1. [`scripts/build_dataset.py`](scripts/build_dataset.py) recorre cada categoría y sus subcategorías, lee los artículos con
   `WikiPage.look_up` (de la biblioteca [esperantilo](https://github.com/jparisu/nlp-esperantilo)) y se queda con los
   párrafos de al menos 30 palabras, con un máximo de 5 por artículo. Espera entre peticiones, reintenta si falla la red y guarda una copia de cada clase por si se interrumpe. Además escribe `dataset/origen.csv` (no se sube al repositorio), con el artículo de Wikipedia del que sale cada párrafo.
2. [`scripts/clean_dataset.py`](scripts/clean_dataset.py) quita los párrafos repetidos, los que aparecen en dos clases a la vez, los que conservan restos de fórmulas LaTeX, enlaces o referencias, y las **referencias bibliográficas** que se cuelan de las secciones *Referencoj* y *Eksteraj ligiloj* (citas del tipo «Kareiva, Peter (1989). "Renewing the Dialogue..."», con ISBN, `et al.`, `pp.`, listas de autores o las marcas «Arkivigite je ... per la retarkivo Wayback Machine» y «Arkivita el la originalo» de los enlaces archivados; eran 21 filas, casi todas en inglés). Con `origen.csv` escribe
   [`dataset/articulos_usados.md`](dataset/articulos_usados.md): los artículos exactos de Wikipedia, con enlace, de los que sale el dataset final.

Los artículos salen de la categoría de partida de cada clase y de sus 10 primeras subcategorías (sin las de `Ĝermoj`, que son esbozos). Se barajan con la semilla 42 y se descargan hasta reunir 400 párrafos por clase. `kemio` se queda en 380 antes de limpiar porque se agotan sus artículos.

Para regenerarlo (tarda unos 45 minutos por los tiempos de espera con Wikipedia):

```
pip install requests git+https://github.com/jparisu/nlp-esperantilo.git
python scripts/build_dataset.py
python scripts/clean_dataset.py
```

### Ruido en las etiquetas

Cada párrafo hereda la etiqueta del artículo del que sale, pero no todos hablan del tema. Por ejemplo, hay un párrafo sobre utensilios de cocina en `fiziko`, uno sobre una sociedad científica y su política pública en `biologio` y uno sobre medicina en `kemio`. Los textos que aparecían en dos clases ya se eliminaron al limpiar el dataset (56 filas).

**Cómo lo medimos.** Con el script [`scripts/medir_ruido.py`](scripts/medir_ruido.py), de forma sencilla:

1. Cada párrafo se pasa por `ciencianlp` y nos quedamos con sus lemas (igual que en el cuaderno).
2. Con **validación cruzada de 5 partes**, cada párrafo lo clasifica un modelo (TF-IDF + regresión logística) que
   **no lo ha visto** al entrenar.
3. Si el modelo predice **otra clase** distinta de la etiqueta, el párrafo es **posible ruido**.

```
python scripts/medir_ruido.py
```

**Resultados:**

| Clase | Posible ruido |
|---|---|
| `biologio` | 15.9 % |
| `fiziko` | 24.2 % |
| `kemio` | 28.2 % |
| **total** | **22.7 %** (249 de 1098 párrafos) |

Es una **cota superior**: incluye los párrafos mal etiquetados, pero también los fallos normales del modelo. Aun así, al leer los ejemplos que muestra el script, varios son ruido de verdad: un párrafo sobre utensilios de cocina en
`fiziko`, uno sobre fe y teología en `biologio`, la biografía de un inventor en `kemio`... Otros son temas de frontera entre disciplinas (la habitabilidad de los planetas en `biologio`, la rutina, un glucósido de las plantas, en `kemio`). Física y química tienen más
ruido que biología porque sus artículos incluyen más temas de frontera entre ellas (química física).

## Estructura del repositorio

```
cienciaNLP/
├── src/ciencianlp/     # la librería
├── tests/              # tests con pytest
├── scripts/            # build_dataset.py, clean_dataset.py y medir_ruido.py
├── dataset/            # dataset.csv y articulos_usados.md
├── notebooks/          # cuaderno de clasificación (fase 3)
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

Cada uno trabaja en su propia rama y entra en `main` con un pull request.

## Licencia y atribución

El código tiene licencia [MIT](LICENSE). Los textos del dataset proceden de la Wikipedia en esperanto y se distribuyen con
su licencia, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
