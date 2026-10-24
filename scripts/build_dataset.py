"""Crea dataset/dataset.csv (text;class) con párrafos de la Wikipedia en esperanto.

Requiere: pip install git+https://github.com/jparisu/nlp-esperantilo.git
"""

import csv
import random
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from esperantilo import WikiPage
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CLASES = {"fiziko": "Kategorio:Fiziko", "biologio": "Kategorio:Biologio", "kemio": "Kategorio:Kemio"}
PARRAFOS_POR_CLASE = 400
MAX_POR_ARTICULO = 5
MIN_PALABRAS = 30
PAUSA = 1  # segundos de cortesía tras cada petición
HILOS = 3  # artículos que se descargan a la vez
MAX_SUBCATEGORIAS = 10  # subcategorías que se miran por clase

# Sesión que reintenta sola (429, 5xx, cortes) esperando cada vez más y respetando Retry-After
SESION = requests.Session()
SESION.headers["User-Agent"] = "ciencianlp-practica/1.0 (https://github.com/danielaagonzalezz/cienciaNLP; proyecto educativo CUNEF)"
SESION.mount("https://", HTTPAdapter(max_retries=Retry(total=6, backoff_factor=2, status_forcelist=(429, 500, 502, 503, 504))))


def miembros(categoria):
    """Devuelve los artículos y las subcategorías de una categoría."""
    time.sleep(PAUSA)
    try:
        lista = SESION.get("https://eo.wikipedia.org/w/api.php", timeout=30,
                           params={"action": "query", "list": "categorymembers", "cmtitle": categoria,
                                   "cmlimit": 500, "format": "json"}).json()["query"]["categorymembers"]
    except (requests.RequestException, ValueError, KeyError):
        raise SystemExit("Sin conexión con Wikipedia: comprueba internet y vuelve a lanzarlo")
    return ([m["title"] for m in lista if m["ns"] == 0],
            [m["title"] for m in lista if m["ns"] == 14 and "Ĝermoj" not in m["title"]])


def parrafos_de(titulo):
    """Párrafos largos de un artículo (lista vacía si no existe o la red falla)."""
    for intento in range(1, 4):
        try:
            pagina = WikiPage.look_up(titulo, language="eo", fallback_languages=(), any_language=False)
        except ValueError:  # la página no existe: no tiene sentido reintentar
            print("saltado:", titulo, "- no existe")
            return []
        except Exception:  # sin red, tiempo agotado, 429...
            print("fallo de red en", titulo, "- reintento", intento)
            time.sleep(20 * intento)
            continue
        time.sleep(PAUSA)
        return [p.replace(";", ",") for texto in pagina.sections.values() for p in texto.split("\n")
                if len(p.split()) >= MIN_PALABRAS and not p.startswith("=")][:MAX_POR_ARTICULO]
    return []


def descargar(categoria):
    """Párrafos de una categoría, con los mismos artículos y orden que descargándolos de uno en uno."""
    articulos, subcategorias = miembros(categoria)
    articulos += [a for sub in subcategorias[:MAX_SUBCATEGORIAS] for a in miembros(sub)[0]]
    articulos = sorted(set(articulos))
    random.Random(42).shuffle(articulos)
    parrafos = []
    with ThreadPoolExecutor(HILOS) as hilos:
        for i in range(0, len(articulos), 2 * HILOS):  # por lotes: conserva el orden y no baja de más
            parrafos += [p for lista in hilos.map(parrafos_de, articulos[i:i + 2 * HILOS]) for p in lista]
            if len(parrafos) >= PARRAFOS_POR_CLASE:
                break
    return parrafos[:PARRAFOS_POR_CLASE]


Path("dataset").mkdir(exist_ok=True)
filas = []
for clase, categoria in CLASES.items():
    parcial = Path(f"dataset/parcial_{clase}.csv")  # copia de seguridad: si ya existe, se reutiliza
    if not parcial.exists():
        with open(parcial, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter=";").writerows([(p,) for p in descargar(categoria)])
    with open(parcial, encoding="utf-8") as f:
        filas += [(fila[0], clase) for fila in csv.reader(f, delimiter=";")]
    print(clase, sum(c == clase for _, c in filas), "párrafos")

with open("dataset/dataset.csv", "w", encoding="utf-8", newline="") as f:
    escritor = csv.writer(f, delimiter=";")
    escritor.writerow(["text", "class"])
    escritor.writerows(filas)
for clase in CLASES:
    Path(f"dataset/parcial_{clase}.csv").unlink()  # ya no hacen falta
