import req


def get_options(form = dict):
    print(form)
    if form["dia"] == '1':
        q_humanas=[]
        q_linguagens=[]
        questions=req.get_exam_by_year(form["ano"])["questions"]
        for x in questions:
            if x["discipline"] == 'linguagens' and x["language"] not in ["ingles","espanhol"]:
                q_linguagens.append(x["index"])
            elif x["discipline"] == 'ciencias-humanas' and x["language"] not in ["ingles","espanhol"]:
                q_humanas.append(x["index"])
        print(q_humanas, q_linguagens)
    elif form["dia"] == '2':
        q_matematica=[]
        q_natureza=[]
        questions=req.get_exam_by_year(form["ano"])["questions"]
        for x in questions:
            if x["discipline"] == 'matematica' and x["language"] not in ["ingles","espanhol"]:
                q_matematica.append(x["index"])
            elif x["discipline"] == 'ciencias-natureza' and x["language"] not in ["ingles","espanhol"]:
                q_natureza.append(x["index"])
        print(q_natureza, q_matematica)