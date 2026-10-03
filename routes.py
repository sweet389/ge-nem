from app import app
from flask import jsonify, render_template, request, redirect, url_for
import IO
from trator import get_options

@app.get("/")
def dashboard():
    # TODO: buscar estatísticas e montar as variáveis
    return render_template(
        "dashboard.html",
        subjects=[], last_attempt=None,
        days_to_enem=0, enem_year=2026, enem_dates_label="",
        redacao_url="https://coredacao.com",
    )


@app.route("/simulado/gerar", methods=["GET", "POST"])
def gerar_simulado():
    if request.method == "POST":
        # TODO: ler request.form, validar, gerar o simulado no backend
        sim_id = get_options(request.form)
        print(request.form)
        return redirect(url_for("simulado", id=sim_id))
    return render_template("gerar_simulado.html")


@app.get("/simulado/<id>")
def simulado(id):
    try:
        IO.read_json(id)
    except FileNotFoundError:
        return "Simulado não encontrado", 404
    return render_template("simulado.html", simulado_id=id, redacao_url="https://coredacao.com")


@app.get("/api/simulados/<id>")
def simulado_json(id):
    try:
        return jsonify(IO.read_json(id))
    except FileNotFoundError:
        return jsonify({"error": "Simulado não encontrado"}), 404


@app.post("/simulado/finalizar")
def finalizar_simulado():
    # TODO: corrigir e salvar o resultado
    sim_id = request.form.get("simulado_id")
    return redirect(url_for("resultado", id=sim_id))


@app.get("/resultado/<id>")
def resultado(id):
    # TODO: buscar o resultado
    return render_template("resultado.html", resultado={})
