from flask import Blueprint, request, render_template, redirect, url_for
from models.repo import ServicesRepo
from models.tables import db, Services
from flask_login import login_required

bp = Blueprint("services", __name__, url_prefix="/services")

repo = ServicesRepo(db)

@bp.get("/")
@login_required
def list_services():
    items = repo.all()
    return render_template("list_services.html", items=items)

@bp.post("/")
@login_required
def create_services():
    name = request.form.get("name")
    opisan = request.form.get("opisan")
    cost = request.form.get("cost")

    repo.add(name, opisan, cost)
    return redirect(url_for("services.list_services"))

@bp.post("/<int:item_id>/delete")
@login_required
def delete_services(item_id):
    item = Services.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("services.list_services"))

@bp.post("/<int:item_id>/update")
@login_required
def update_services(item_id):
    item = Services.query.get_or_404(item_id)
    item.name = request.form.get("name", item.name)
    item.opisan = request.form.get("opisan", item.opisan)
    item.cost = request.form.get("cost", item.cost)
    db.session.commit()
    return redirect(url_for("services.list_services"))
