#!/usr/bin/env python3
"""Construye el dataset de clasificación de textos en Esperanto (ciencia).

Recupera artículos de la Wikipedia en Esperanto de las categorías elegidas,
los divide en párrafos, los limpia y genera un CSV conforme al contrato de datos:
UTF-8, separador ';', cabecera ``text;class``, un párrafo por fila, sin ';',
sin HTML, enlaces ni referencias.

Clases: fiziko (física), biologio (biología), kemio (química).

Uso:
    python scripts/build_dataset.py
    python scripts/build_dataset.py --per-class 400 --out data/dataset.csv

Dependencias: requests.
"""
from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from collections import deque
from pathlib import Path

import requests

API_URL = "https://eo.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "CUNEF-MineriaTextos-Practica/1.0 (proyecto educativo)"}
TIMEOUT = 30
MAX_CANDIDATES = 1000  # artículos que se recogen como máximo por clase

# Clase -> categorías semilla en la Wikipedia en Esperanto.
# Si una clase sale vacía, comprobad el nombre de la categoría.
SEED_CATEGORIES = {
    "fiziko": ["Kategorio:Fiziko"],
    "biologio": ["Kategorio:Biologio"],
    "kemio": ["Kategorio:Kemio"],
}

# Secciones finales sin prosa (referencias, enlaces...): se descartan.
STOP_SECTIONS = {
    "referencoj", "notoj", "eksteraj ligiloj", "vidu ankaŭ", "bibliografio",
    "fontoj", "literaturo", "ligiloj", "legaĵoj",
}

HTML_TAG = re.compile(r"<[^>]+>")
URL = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
REFERENCE = re.compile(r"\[[^\]]{0,40}\]")
HEADING = re.compile(r"^=+\s*(.+?)\s*=+$")
SPACES = re.compile(r"\s+")


def api_get(params: dict) -> dict:
    params = {**params, "format": "json", "formatversion": 2}
    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def category_members(category: str, namespace: int) -> list[str]:
    """Títulos de artículos (namespace 0) o subcategorías (namespace 14)."""
    members: list[str] = []
    params = {"action": "query", "list": "categorymembers", "cmtitle": category,
              "cmnamespace": namespace, "cmlimit": 500}
    while True:
        data = api_get(params)
        members += [m["title"] for m in data.get("query", {}).get("categorymembers", [])]
        token = data.get("continue", {}).get("cmcontinue")
        if not token:
            return members
        params = {**params, "cmcontinue": token}


def collect_titles(seeds: list[str], depth: int) -> list[str]:
    """Artículos de las categorías semilla y sus subcategorías (hasta ``depth``)."""
    titles: dict[str, None] = {}
    visited: set[str] = set()
    queue = deque((seed, 0) for seed in seeds)
    while queue and len(titles) < MAX_CANDIDATES:
        category, level = queue.popleft()
        if category in visited:
            continue
        visited.add(category)
        for title in category_members(category, namespace=0):
            titles.setdefault(title)
        if level < depth:
            queue.extend((sub, level + 1) for sub in category_members(category, namespace=14))
    return list(titles)


def get_extract(title: str) -> str:
    """Texto plano del artículo; las secciones aparecen como ``== Título ==``."""
    data = api_get({"action": "query", "prop": "extracts", "explaintext": 1,
                    "exsectionformat": "wiki", "redirects": 1, "titles": title})
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        return ""
    return pages[0].get("extract", "") or ""


def clean_paragraph(raw: str, min_chars: int = 100) -> str | None:
    """Limpia un párrafo (HTML, enlaces, referencias, ';'). None si no sirve."""
    text = html.unescape(raw)
    text = HTML_TAG.sub(" ", text)
    text = URL.sub(" ", text)
    text = REFERENCE.sub("", text)
    text = text.replace(";", ",")
    text = SPACES.sub(" ", text).strip()
    if len(text) < min_chars or text[-1] not in ".!?\"”»)":
        return None  # titulares, listas y fragmentos sueltos
    return text


def split_paragraphs(extract: str) -> list[str]:
    paragraphs: list[str] = []
    for line in extract.splitlines():
        line = line.strip()
        if not line:
            continue
        heading = HEADING.match(line)
        if heading:
            if heading.group(1).strip().lower() in STOP_SECTIONS:
                break
            continue
        cleaned = clean_paragraph(line)
        if cleaned:
            paragraphs.append(cleaned)
    return paragraphs


def build_rows(per_class: int, depth: int) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for label, seeds in SEED_CATEGORIES.items():
        titles = collect_titles(seeds, depth)
        if not titles:
            print(f"[AVISO] '{label}': sin artículos con {seeds}.", file=sys.stderr)
        count = 0
        for title in titles:
            if count >= per_class:
                break
            try:
                paragraphs = split_paragraphs(get_extract(title))
            except requests.RequestException as exc:
                print(f"[AVISO] Se omite '{title}': {exc}", file=sys.stderr)
                continue
            for paragraph in paragraphs[: per_class - count]:
                rows.append((paragraph, label))
                count += 1
        print(f"[{label}] {count} párrafos")
        if count < per_class:
            print(f"[AVISO] '{label}' tiene menos de {per_class} párrafos.", file=sys.stderr)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=Path("data/dataset.csv"))
    parser.add_argument("--per-class", type=int, default=500,
                        help="párrafos por clase (la práctica recomienda más de 300)")
    parser.add_argument("--depth", type=int, default=1,
                        help="profundidad de subcategorías a recorrer")
    args = parser.parse_args()

    rows = build_rows(args.per_class, args.depth)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(["text", "class"])
        writer.writerows(rows)
    print(f"Dataset escrito en {args.out} ({len(rows)} párrafos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
