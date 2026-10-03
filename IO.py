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


def read_json(simulado_id):
    file = Path("json") / str(simulado_id)
    if not file.is_file():
        raise FileNotFoundError(f"Simulado não encontrado: {simulado_id}")
    with file.open(encoding="utf-8") as f:
        return json.load(f)
    
