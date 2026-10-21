# ciencianlp

Librería de NLP **basada en reglas** para esperanto, construida desde cero (sin spaCy, NLTK ni
Stanza) con una API similar a la de spaCy. Forma parte de la práctica de Minería de Textos:
clasificar textos en esperanto por temática científica (física, biología y química).

## Instalación

```
pip install git+https://github.com/danielaagonzalezz/cienciaNLP.git
```

## Uso

```python
import ciencianlp

ciencianlp.__version__   # '0.1.0'
```

!!! note "En desarrollo"
    Esta página se irá completando a medida que se implementen el tokenizador, el
    lematizador, el etiquetador gramatical, las stop-words y los objetos `Doc` y `Token`.
    La [referencia de la API](api.md) se genera sola a partir de los *docstrings* del código.

## Qué incluirá

| Componente | Función |
|---|---|
| Tokenizador | Divide un texto en tokens |
| Lematizador | Obtiene el lema de cada palabra |
| Etiquetador POS | Asigna la categoría gramatical |
| Stop-words | Identifica palabras vacías |
| `Doc` / `Token` | Estructuran el resultado del análisis |

## Código fuente y licencia

El código está en [GitHub](https://github.com/danielaagonzalezz/cienciaNLP) bajo licencia MIT.
Los textos del dataset proceden de la Wikipedia en esperanto (licencia CC BY-SA).
