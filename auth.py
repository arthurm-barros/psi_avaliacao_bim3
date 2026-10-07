from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        database.criar_usuario(
            request.form.get('nome'),
            request.form.get('email'),
            generate_password_hash(request.form.get('senha')),
        )
        return redirect(url_for('auth.login'))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = database.buscar_usuario_por_email(request.form.get('email'))
        if usuario is not None:
            if check_password_hash(usuario.senha_hash, request.form.get('senha')):
                session['usuario_id'] = usuario.id
                session['usuario_nome'] = usuario.nome
                return redirect(url_for('index'))
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop('usuario_id')
    session.pop('usuario_nome')
    return redirect(url_for("auth.login"))