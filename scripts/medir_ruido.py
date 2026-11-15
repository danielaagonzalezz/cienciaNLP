"""Mide el ruido de las etiquetas de dataset/dataset.csv de forma sencilla.

Idea: con validación cruzada, cada párrafo lo clasifica un modelo que NO lo ha visto al entrenar.
Si el modelo predice otra clase distinta de su etiqueta, el párrafo es posible ruido.

Es una cota superior: incluye los párrafos mal etiquetados, pero también los fallos normales del modelo.
Los párrafos se procesan con ciencianlp igual que en el cuaderno (lemas de sustantivos, adjetivos,
verbos y X, sin stop-words).

Uso: python scripts/medir_ruido.py   (requiere pandas, scikit-learn y la librería ciencianlp)
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

from ciencianlp import nlp

POS_TAGS = {"NOUN", "ADJ", "VERB", "X"}


def lemas(texto):
    """Lemas de las palabras que aportan información sobre el tema (igual que words_of en el cuaderno)."""
    return [t.lemma_ for t in nlp(texto) if t.is_alpha and not t.is_stop and t.pos_ in POS_TAGS]


df = pd.read_csv("dataset/dataset.csv", sep=";")

# Cada párrafo se predice con un modelo entrenado con el resto (validación cruzada de 5 partes)
X = TfidfVectorizer(analyzer=lemas, min_df=3).fit_transform(df["text"])
df["prediccion"] = cross_val_predict(LogisticRegression(C=10, max_iter=1000), X, df["class"], cv=5)
df["posible_ruido"] = df["prediccion"] != df["class"]

print("% de párrafos que son posible ruido:")
print((df.groupby("class")["posible_ruido"].mean() * 100).round(1))
print(f"total: {df['posible_ruido'].mean() * 100:.1f} % ({df['posible_ruido'].sum()} de {len(df)} párrafos)")

print("\nA qué clase los manda el modelo (filas: etiqueta, columnas: predicción):")
print(pd.crosstab(df["class"], df["prediccion"]))

print("\nAlgunos ejemplos:")
ejemplos = df[df["posible_ruido"]].sample(8, random_state=42)
for _, fila in ejemplos.iterrows():
    print(f"[{fila['class']} -> {fila['prediccion']}] {fila['text'][:150]}...")
