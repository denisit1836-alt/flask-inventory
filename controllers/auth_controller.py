from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import UserRepo

bp = Blueprint("auth", __name__, url_prefix="/auth")
repo = UserRepo()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Заполните все поля", "error")
            return redirect(url_for("auth.login"))

        user = repo.get_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            flash("Успешный вход!", "success")
            return redirect(url_for("index"))
        else:
            flash("Неверный логин или пароль", "error")

    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Заполните все поля", "error")
            return redirect(url_for("auth.register"))

        if repo.get_by_username(username):
            flash("Пользователь уже существует", "error")
        else:
            repo.add(username, password)
            flash("Регистрация успешна! Теперь войдите.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("auth.login"))
