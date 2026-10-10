import json
import req
import datetime
from pathlib import Path


def gen_json(lista):
    date = datetime.datetime.now()
    content={}
    simulado_id = date.strftime("%Y%m%d%H%M%S%f")
    file = Path("json") / simulado_id
    file.parent.mkdir(exist_ok=True)
    with file.open("w", encoding="utf-8") as f:
        for x in lista:
            content[len(content)]=x
        json.dump(content, f, indent=2, ensure_ascii=False)
    return simulado_id
        

def gen_discipline_questions(year, indexs, limite1, limite2):
    ch=[]
    mt=[]
    nt=[]
    ln=[]
    print("IO",indexs)
    for key, index in indexs.items():
        if key == "natureza":
            for x in index:
                if limite1 > len(nt):
                    nt.append(req.get_exam_question_by_index(year,str(x)))
        if key == "matematica":
            for x in index:
                if limite2 > len(mt):
                    mt.append(req.get_exam_question_by_index(year,str(x)))
        if key == "linguagens":
            for x in index:
                if limite1 > len(ln):
                    ln.append(req.get_exam_question_by_index(year,str(x)))
        if key == "ciencias-humanas":
            for x in index:
                if limite2 > len(ch):
                    ch.append(req.get_exam_question_by_index(year,str(x))) 
    return gen_json(ch+ln+mt+nt)


_DISCIPLINE_LABELS = {
    "ciencias-humanas": "Ciências Humanas",
    "ciencias-natureza": "Ciências da Natureza",
    "linguagens": "Linguagens",
    "matematica": "Matemática",
}


def read_json(simulado_id):
    file = Path("json") / str(simulado_id)
    if not file.is_file():
        raise FileNotFoundError(f"Simulado não encontrado: {simulado_id}")
    with file.open(encoding="utf-8") as f:
        return json.load(f)


def answers_path(simulado_id):
    return Path("json") / f"{simulado_id}_answers"


def save_answers(simulado_id, answers):
    """Salva as alternativas marcadas (dict index -> letra) do simulado."""
    file = answers_path(simulado_id)
    file.parent.mkdir(exist_ok=True)
    with file.open("w", encoding="utf-8") as f:
        json.dump(answers or {}, f, indent=2, ensure_ascii=False)
    return simulado_id


def read_answers(simulado_id):
    file = answers_path(simulado_id)
    if not file.is_file():
        return {}
    with file.open(encoding="utf-8") as f:
        return json.load(f)


def build_result(simulado_id):
    """Corrige o simulado e devolve o resumo + a revisão questão a questão."""
    questions = read_json(simulado_id)
    answers = read_answers(simulado_id)

    revisao = []
    materias = {}
    acertos = 0

    for position, question in sorted(questions.items(), key=lambda item: int(item[0])):
        correct = question.get("correctAlternative")
        chosen = answers.get(str(question.get("index", position)))
        is_correct = chosen == correct
        acertos += 1 if is_correct else 0

        discipline = question.get("discipline") or "outros"
        materia = materias.setdefault(
            discipline,
            {"nome": _DISCIPLINE_LABELS.get(discipline, discipline), "total": 0, "acertos": 0, "erros": 0},
        )
        materia["total"] += 1
        materia["acertos"] += 1 if is_correct else 0
        materia["erros"] += 0 if is_correct else 1

        alternatives = question.get("alternatives", [])
        chosen_text = next((a.get("text") for a in alternatives if a.get("letter") == chosen), None)
        correct_text = next((a.get("text") for a in alternatives if a.get("letter") == correct), None)

        files = question.get("files") or []
        revisao.append({
            "numero": len(revisao) + 1,
            "index": question.get("index", position),
            "materia": _DISCIPLINE_LABELS.get(discipline, discipline),
            "context": question.get("context"),
            "imagem": files[0] if files else None,
            "enunciado": question.get("alternativesIntroduction"),
            "respondido": chosen,
            "respondido_texto": chosen_text,
            "correta": correct,
            "correta_texto": correct_text,
            "acertou": is_correct,
        })

    for materia in materias.values():
        materia["percentual"] = round(materia["acertos"] / materia["total"] * 100) if materia["total"] else 0

    total = len(revisao)
    return {
        "id": simulado_id,
        "total": total,
        "acertos": acertos,
        "erros": total - acertos,
        "percentual": round(acertos / total * 100) if total else 0,
        "materias": list(materias.values()),
        "revisao": revisao,
    }
    
