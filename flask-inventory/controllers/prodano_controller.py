from flask import Blueprint, request, render_template, redirect, url_for
from models.repo import ProdanoRepo
from models.tables import db, Prodano, Tovar, Services
from flask_login import login_required

bp = Blueprint("prodano", __name__, url_prefix="/prodano")

repo = ProdanoRepo(db)

@bp.get("/")
@login_required
def list_prodano():
    items = repo.all()
    tovars = Tovar.query.all()
    uslugi = Services.query.all()
    return render_template("list_prodano.html", items=items, tovars=tovars, uslugi=uslugi)

@bp.post("/")
@login_required
def create_prodano():
    tovar_name = request.form.get("tovar_name")
    usluga_name = request.form.get("usluga_name")  # Может быть пусто
    personal = request.form.get("personal")
    date = request.form.get("date")

    # Получаем объекты для расчёта стоимости
    tovar = Tovar.query.filter_by(name=tovar_name).first()
    usluga = Services.query.filter_by(name=usluga_name).first() if usluga_name else None

    # Рассчитываем стоимость на сервере
    tovar_cost = float(tovar.cost) if tovar else 0.0
    usluga_cost = float(usluga.cost) if usluga else 0.0
    total_cost = tovar_cost + usluga_cost

    # Сохраняем запись
    new_item = Prodano(
        name=tovar_name,
        usluga_name=usluga_name or None,
        personal=personal,
        cost=str(total_cost),  # Точная сумма
        date=date
    )
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for("prodano.list_prodano"))

@bp.post("/<int:item_id>/update")
@login_required
def update_prodano(item_id):
    item = Prodano.query.get_or_404(item_id)

    tovar_name = request.form.get("tovar_name")
    usluga_name = request.form.get("usluga_name")
    personal = request.form.get("personal")
    date = request.form.get("date")

    # Получаем объекты для расчёта
    tovar = Tovar.query.filter_by(name=tovar_name).first()
    usluga = Services.query.filter_by(name=usluga_name).first() if usluga_name else None

    tovar_cost = float(tovar.cost) if tovar else 0.0
    usluga_cost = float(usluga.cost) if usluga else 0.0
    total_cost = tovar_cost + usluga_cost

    # Обновляем запись
    item.name = tovar_name
    item.usluga_name = usluga_name or None
    item.personal = personal
    item.cost = str(total_cost)
    item.date = date

    db.session.commit()
    return redirect(url_for("prodano.list_prodano"))

@bp.post("/<int:item_id>/delete")
@login_required
def delete_prodano(item_id):
    item = Prodano.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("prodano.list_prodano"))
