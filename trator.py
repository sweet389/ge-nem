import req
import IO
import random

def get_options(form):
    day = form.get("dia")
    year = form.get("ano")
    if day == "1":
        return IO.gen_discipline_questions(
            year,
            __dia1__(form),
            int(form.get("linguagens", 0)),
            int(form.get("humanas", 0)),
        )
    if day == "2":
        return IO.gen_discipline_questions(
            year,
            __dia2__(form),
            int(form.get("natureza", 0)),
            int(form.get("matematica", 0)),
        )
    raise ValueError("Dia do simulado inválido")
        
def __dia1__(form):
        q_humanas=[]
        q_linguagens=[]
        questions=req.get_exam_by_year(form["ano"])["questions"]
        for x in questions:
            if x["discipline"] == 'linguagens' and x["language"] not in ["ingles","espanhol"]:
                q_linguagens.append(x["index"])
            elif x["discipline"] == 'ciencias-humanas' and x["language"] not in ["ingles","espanhol"]:
                q_humanas.append(x["index"])
        #print(q_humanas, q_linguagens)
        random.shuffle(q_humanas)
        random.shuffle(q_linguagens)
        return {"ciencias-humanas": q_humanas,"linguagens": q_linguagens}
    
def __dia2__(form): 
        q_matematica=[]
        q_natureza=[]
        questions=req.get_exam_by_year(form["ano"])["questions"]
        for x in questions:
            if x["discipline"] == 'matematica' and x["language"] not in ["ingles","espanhol"]:
                q_matematica.append(x["index"])
            elif x["discipline"] == 'ciencias-natureza' and x["language"] not in ["ingles","espanhol"]:
                q_natureza.append(x["index"])
        #print(q_natureza, q_matematica)
        random.shuffle(q_natureza)
        random.shuffle(q_matematica)
        return {"natureza": q_natureza,"matematica": q_matematica}