import json
from pathlib import Path


STATUS_FILE = Path(__file__).parent / "status" / "carol.json"


def update_status(dia, first, second):
    file = STATUS_FILE
    file.parent.mkdir(exist_ok=True)
    with file.open("r", encoding="utf-8") as f:
        dados = json.load(f)
    if dia == 1:
        dados["linguagens"] = first
        dados["cienciasH"] = second
    elif dia == 2:
        dados["matematica"] = first
        dados["cienciasN"] = second
    with file.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def gerar_status(dict):
    ch = 0
    lin = 0
    cn = 0
    mt = 0
    for id in dict["materias"]:
        if id["nome"] == "Ciências Humanas":
            ch = id["percentual"]
        if id["nome"] == "Linguagens":
            lin = id["percentual"]
        if id["nome"] == "Ciências da Natureza":
            cn = id["percentual"]
        if id["nome"] == "Matemática":
            mt = id["percentual"]

    names = {id["nome"] for id in dict["materias"]}
    if {"Matemática", "Ciências da Natureza"}.issubset(names):
        update_status(2, cn, mt)
    if {"Linguagens", "Ciências Humanas"}.issubset(names):
        update_status(1, ch, lin)
    