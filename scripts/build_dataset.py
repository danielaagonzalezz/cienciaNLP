"""Crea dataset/dataset.csv (text;class) con párrafos de la Wikipedia en esperanto.

Requiere: pip install git+https://github.com/jparisu/nlp-esperantilo.git
"""

import csv
import random
import time
from pathlib import Path

import requests
from esperantilo import WikiPage

CLASES = {"fiziko": "Kategorio:Fiziko", "biologio": "Kategorio:Biologio", "kemio": "Kategorio:Kemio"}
PARRAFOS_POR_CLASE = 20
MAX_POR_ARTICULO = 5
MIN_PALABRAS = 30
PAUSA = 5  # segundos entre peticiones
MAX_SUBCATEGORIAS = 10  # subcategorías que se miran por clase


def miembros(categoria):
    """Devuelve los artículos y las subcategorías de una categoría."""
    for intento in range(1, 7):
        time.sleep(PAUSA)
        r = requests.get("https://eo.wikipedia.org/w/api.php", timeout=30,
                         headers={"User-Agent": "ciencianlp-practica/1.0 (https://github.com/danielaagonzalezz/cienciaNLP; proyecto educativo CUNEF)"},
                         params={"action": "query", "list": "categorymembers", "cmtitle": categoria,
                                 "cmlimit": 500, "format": "json"})
        if r.status_code == 200 and r.text.startswith("{"):
            break
        espera = max(int(r.headers.get("Retry-After", 0)), 15 * intento)  # Wikipedia dice cuánto esperar
        print("reintento", intento, categoria, "- código", r.status_code, "- espero", espera, "s")
        time.sleep(espera)
    lista = r.json()["query"]["categorymembers"]
    return ([m["title"] for m in lista if m["ns"] == 0],
            [m["title"] for m in lista if m["ns"] == 14 and "Ĝermoj" not in m["title"]])


filas = []
for clase, categoria in CLASES.items():
    articulos, subcategorias = miembros(categoria)
    for sub in subcategorias[:MAX_SUBCATEGORIAS]:
        articulos += miembros(sub)[0]
    articulos = sorted(set(articulos))
    random.Random(42).shuffle(articulos)

    n = 0
    for titulo in articulos:
        if n >= PARRAFOS_POR_CLASE:
            break
        try:
            pagina = WikiPage.look_up(titulo, language="eo", fallback_languages=(), any_language=False)
        except Exception as error:
            print("saltado:", titulo, error)
            time.sleep(PAUSA)
            continue
        time.sleep(PAUSA)
        parrafos = [p.replace(";", ",") for texto in pagina.sections.values() for p in texto.split("\n")
                    if len(p.split()) >= MIN_PALABRAS and not p.startswith("=")]
        for p in parrafos[:MAX_POR_ARTICULO][:PARRAFOS_POR_CLASE - n]:
            filas.append((p, clase))
            n += 1
    print(clase, n, "párrafos")

Path("dataset").mkdir(exist_ok=True)
with open("dataset/dataset.csv", "w", encoding="utf-8", newline="") as f:
    escritor = csv.writer(f, delimiter=";")
    escritor.writerow(["text", "class"])
    escritor.writerows(filas)