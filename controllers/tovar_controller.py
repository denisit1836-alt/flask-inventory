from flask import Blueprint, request, render_template, redirect, url_for
from models.repo import TovarRepo  
from models.tables import db, Tovar  
from flask_login import login_required

bp = Blueprint("tovar", __name__, url_prefix="/tovar")  

repo = TovarRepo(db)

@bp.get("/")
@login_required
def list_tovar():  
    tovars = repo.all()
    return render_template("list_tovar.html", tovars=tovars)  

@bp.post("/")
def create_tovar():  
    name = request.form.get("name")
    kategor = request.form.get("kategor")
    proizv = request.form.get("proizv")
    strana = request.form.get("strana")
    cost = request.form.get("cost")
    kol_vo = request.form.get("kol_vo")
    repo.add(name, kategor, proizv, strana, cost, kol_vo)
    return redirect(url_for("tovar.list_tovar"))  

@bp.post("/<int:tovar_id>/delete")
def delete_tovar(tovar_id):  
    tovar = Tovar.query.get_or_404(tovar_id)
    db.session.delete(tovar)
    db.session.commit()
    return redirect(url_for("tovar.list_tovar"))

@bp.post("/<int:tovar_id>/update")
def update_tovar(tovar_id):  
    tovar = Tovar.query.get_or_404(tovar_id)
    tovar.name = request.form.get("name", tovar.name)
    tovar.kategor = request.form.get("kategor", tovar.kategor)
    tovar.proizv = request.form.get("proizv", tovar.proizv)
    tovar.strana = request.form.get("strana", tovar.strana)
    tovar.cost = request.form.get("cost", tovar.cost)
    tovar.kol_vo = request.form.get("kol_vo", tovar.kol_vo)
    db.session.commit()
    return redirect(url_for("tovar.list_tovar"))
