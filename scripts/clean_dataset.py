"""Limpia dataset/dataset.csv: quita repetidos, textos en dos clases y restos de fórmulas o enlaces.

Guarda una copia del original en dataset/dataset_bruto.csv (no se sube al repositorio).
Uso: python scripts/clean_dataset.py
"""

import csv
import re
import shutil
from collections import Counter
from pathlib import Path

RUTA = Path("dataset/dataset.csv")
BRUTO = Path("dataset/dataset_bruto.csv")

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