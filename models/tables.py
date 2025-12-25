from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Tovar(db.Model):
    __tablename__ = 'tovar'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    kategor = db.Column(db.String(100), nullable=False)
    proizv = db.Column(db.String(50), nullable=False)
    strana = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    kol_vo = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Tovar {self.name}>'

class Prodano(db.Model):
    __tablename__ = 'prodano'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    usluga_name = db.Column(db.String(50), nullable=True)
    personal = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Prodano {self.name}>'

class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    opisan = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return f'<Services {self.name}>'
