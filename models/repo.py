from models.tables import db, Tovar, Prodano, Services

class TovarRepo:
    def __init__(self, db_instance=None):
        if db_instance:
            global db
            db = db_instance

    def all(self):
        return Tovar.query.all()

    def add(self, name, kategor, proizv, strana, cost, kol_vo):
        new = Tovar(name=name, kategor=kategor, proizv=proizv, strana=strana, cost=cost, kol_vo=kol_vo)
        db.session.add(new)
        db.session.commit()
        return new

class ProdanoRepo:
    def __init__(self, db_instance=None):
        if db_instance:
            global db
            db = db_instance

    def all(self):
        return Prodano.query.all()

    def add(self, name, personal, cost, date):
        new = Prodano(name=name, personal=personal, cost=cost, date=date)
        db.session.add(new)
        db.session.commit()
        return new

class ServicesRepo:
    def __init__(self, db_instance=None):
        if db_instance:
            global db
            db = db_instance

    def all(self):
        return Services.query.all()

    def add(self, name, opisan, cost):
        new = Services(name=name, opisan=opisan, cost=cost)
        db.session.add(new)
        db.session.commit()
        return new
