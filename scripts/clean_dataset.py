"""Limpia dataset/dataset.csv: quita repetidos, textos en dos clases y restos de fórmulas o enlaces.

Guarda una copia del original en dataset/dataset_bruto.csv (no se sube al repositorio).
Con dataset/origen.csv (lo crea build_dataset.py) escribe dataset/articulos_usados.md:
los artículos de Wikipedia de los que sale cada párrafo que queda en el dataset.
Uso: python scripts/clean_dataset.py
"""

import csv
import re
import shutil
from collections import Counter
from pathlib import Path
from urllib.parse import quote

RUTA = Path("dataset/dataset.csv")
BRUTO = Path("dataset/dataset_bruto.csv")
ORIGEN = Path("dataset/origen.csv")
USADOS = Path("dataset/articulos_usados.md")

if not BRUTO.exists():  # la primera vez, guardar el original
    shutil.copy(RUTA, BRUTO)

with open(BRUTO, encoding="utf-8", newline="") as f:
    filas = list(csv.reader(f, delimiter=";"))[1:]

clases_de = {}  # en qué clases aparece cada texto
for texto, clase in filas:
    clases_de.setdefault(texto, set()).add(clase)

sucio = re.compile(r"\\|[{}]|https?://|www\.|\[\d+\]|<[a-z/]")  # LaTeX, enlaces, referencias, HTML
limpias, vistos, descartadas = [], set(), Counter()
for texto, clase in filas:
    if len(clases_de[texto]) > 1:
        descartadas["aparece en dos clases"] += 1
    elif texto in vistos:
        descartadas["repetido"] += 1
    elif sucio.search(texto):
        descartadas["fórmula, enlace o referencia"] += 1
    else:
        vistos.add(texto)
        limpias.append((texto, clase))

with open(RUTA, "w", encoding="utf-8", newline="") as f:
    escritor = csv.writer(f, delimiter=";", lineterminator="\n")
    escritor.writerow(["text", "class"])
    escritor.writerows(limpias)

print("Descartadas:", dict(descartadas))
print("Quedan", len(limpias), "filas:", dict(Counter(c for _, c in limpias)))

if ORIGEN.exists():  # lista de artículos de los que sale lo que queda en el dataset
    with open(ORIGEN, encoding="utf-8", newline="") as f:
        articulo_de = {}
        for texto, clase, articulo in list(csv.reader(f, delimiter=";"))[1:]:
            articulo_de.setdefault((texto, clase), articulo)
    parrafos = {}  # clase -> artículo -> nº de párrafos
    for texto, clase in limpias:
        articulo = articulo_de[(texto, clase)]
        parrafos.setdefault(clase, Counter())[articulo] += 1
    lineas = ["# Artículos de los que sale el dataset", "",
              "Lista exacta de los artículos de la Wikipedia en esperanto que aportan al menos un párrafo a "
              "`dataset/dataset.csv` (ya limpio). La genera `scripts/clean_dataset.py` a partir de "
              "`dataset/origen.csv`, que escribe `scripts/build_dataset.py`.", ""]
    for clase, articulos in parrafos.items():
        lineas += [f"## {clase}: {len(articulos)} artículos, {sum(articulos.values())} párrafos", ""]
        lineas += [f"- [{a}](https://eo.wikipedia.org/wiki/{quote(a.replace(' ', '_'))}): {n}"
                   for a, n in sorted(articulos.items())]
        lineas.append("")
    USADOS.write_text("\n".join(lineas), encoding="utf-8")
    print("Escrito", USADOS)
