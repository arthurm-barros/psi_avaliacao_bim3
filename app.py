import math

from flask import Flask, flash, redirect, render_template, request, session, url_for

import database, auth
from utils import proteger_com_login

app = Flask(__name__)
app.secret_key = 'zyxwvutsrqponmlkjihgfedcba'
app.register_blueprint(auth.auth_bp)

database.criar_banco()

@proteger_com_login
@app.route("/")
def index():
    treinos = database.listar_treinos()
    return render_template("index.html", treinos=treinos)


@proteger_com_login
@app.route("/treinos/novo", methods=["GET", "POST"])
def novo_treino():
    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        duracao = int(request.form["duracao"])
        database.criar_treino(titulo, tipo, duracao, session['usuario_id'])
        flash("Treino cadastrado.")
        return redirect(url_for("index"))

    return render_template("novo_treino.html")


@proteger_com_login
@app.route("/treinos/<int:treino_id>/editar", methods=["GET", "POST"])
def editar_treino(treino_id):
    treino = database.buscar_treino(treino_id)
    if treino is None:
        return "Treino não encontrado", 404

    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        duracao = int(request.form["duracao"])
        if 'usuario_id' in treino and treino['usuario_id'] != session['usuario_id']:
            return 'Você não tem permissão para editar este treino', 403
        database.atualizar_treino(treino_id, titulo, tipo, duracao)
        flash("Treino atualizado.")
        return redirect(url_for("index"))

    return render_template("editar_treino.html", treino=treino)


@proteger_com_login
@app.post("/treinos/<int:treino_id>/concluir")
def concluir_treino(treino_id):
    treino =  database.buscar_treino(treino_id)
    if treino is None:
            return 'Treino não encontrado', 404
    if 'usuario_id' in treino and treino['usuario_id'] != session['usuario_id']:
        return 'Você não tem permissão para editar este treino', 403
    database.alternar_concluido(treino_id)
    flash("Status do treino atualizado.")
    return redirect(url_for("index"))


@proteger_com_login
@app.post("/treinos/<int:treino_id>/excluir")
def excluir_treino(treino_id):
    treino =  database.buscar_treino(treino_id)
    if treino is None:
        return 'Treino não encontrado', 404
    if 'usuario_id' in treino and treino['usuario_id'] != session['usuario_id']:
        return 'Você não tem permissão para excluir este treino', 403
    database.excluir_treino(treino_id)
    flash("Treino excluído.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
