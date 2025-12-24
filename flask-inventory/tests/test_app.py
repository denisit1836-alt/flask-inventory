import pytest
from app import app, db
from models.tables import Tovar, Prodano, Services

@pytest.fixture
def app_context():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()



def test_tovar_model_create(app_context):
    tovar = Tovar(name='Тестовый товар', kategor='Категория', proizv='Производитель',
                  strana='Страна', cost='1000', kol_vo='10')
    db.session.add(tovar)
    db.session.commit()
    assert Tovar.query.count() == 1
    assert Tovar.query.first().name == 'Тестовый товар'

def test_tovar_model_fields(app_context):
    tovar = Tovar(name='Проверка полей', kategor='Тест', proizv='Т', strana='Т', cost='500', kol_vo='5')
    db.session.add(tovar)
    db.session.commit()
    item = Tovar.query.first()
    assert item.kategor == 'Тест'
    assert item.cost == '500'

def test_tovar_model_update(app_context):
    tovar = Tovar(name='Старое', kategor='Старая', proizv='С', strana='С', cost='100', kol_vo='1')
    db.session.add(tovar)
    db.session.commit()

    tovar.cost = '9999'
    db.session.commit()
    assert Tovar.query.first().cost == '9999'

def test_tovar_model_delete(app_context):
    tovar = Tovar(name='Удалить', kategor='Т', proizv='Т', strana='Т', cost='1', kol_vo='1')
    db.session.add(tovar)
    db.session.commit()
    count_before = Tovar.query.count()

    db.session.delete(tovar)
    db.session.commit()
    assert Tovar.query.count() == count_before - 1

def test_multiple_tovar(app_context):
    for i in range(5):
        db.session.add(Tovar(name=f'Товар {i}', kategor='Т', proizv='Т', strana='Т', cost='100', kol_vo='1'))
    db.session.commit()
    assert Tovar.query.count() == 5

# Prodano
def test_prodano_create(app_context):
    item = Prodano(name='Продажа 1', personal='Иванов', cost=5000, date='2025-12-18')
    db.session.add(item)
    db.session.commit()
    assert Prodano.query.count() == 1

def test_prodano_fields(app_context):
    item = Prodano(name='Тест', personal='Петров', cost=3000, date='2025-12-18')
    db.session.add(item)
    db.session.commit()
    assert Prodano.query.first().personal == 'Петров'

def test_prodano_update(app_context):
    item = Prodano(name='Старая', personal='А', cost=100, date='2025-01-01')
    db.session.add(item)
    db.session.commit()

    item.cost = 9999
    db.session.commit()
    assert Prodano.query.first().cost == 9999

def test_prodano_delete(app_context):
    item = Prodano(name='Удалить', personal='Т', cost=1, date='2025-01-01')
    db.session.add(item)
    db.session.commit()
    db.session.delete(item)
    db.session.commit()
    assert Prodano.query.count() == 0

# Services
def test_services_create(app_context):
    item = Services(name='Ремонт', tovar='Ноутбук', opisan='Замена экрана', cost='5000', date='2025-12-18')
    db.session.add(item)
    db.session.commit()
    assert Services.query.count() == 1

def test_services_fields(app_context):
    item = Services(name='Услуга', tovar='Телефон', opisan='Ремонт', cost='2000', date='2025-12-18')
    db.session.add(item)
    db.session.commit()
    assert Services.query.first().opisan == 'Ремонт'

def test_services_update(app_context):
    item = Services(name='Старая', tovar='Т', opisan='Старая', cost='100', date='2025-01-01')
    db.session.add(item)
    db.session.commit()

    item.cost = '8000'
    db.session.commit()
    assert Services.query.first().cost == '8000'

def test_services_delete(app_context):
    item = Services(name='Удалить', tovar='Т', opisan='Т', cost='1', date='2025-01-01')
    db.session.add(item)
    db.session.commit()
    db.session.delete(item)
    db.session.commit()
    assert Services.query.count() == 0


def test_all_tables_empty_after_drop(app_context):
    assert Tovar.query.count() == 0
    assert Prodano.query.count() == 0
    assert Services.query.count() == 0

def test_tovar_repr(app_context):
    tovar = Tovar(name='Тест repr', kategor='Т', proizv='Т', strana='Т', cost='1', kol_vo='1')
    db.session.add(tovar)
    db.session.commit()
    assert 'Тест repr' in str(tovar)

def test_prodano_repr(app_context):
    item = Prodano(name='Продажа repr', personal='Т', cost=1, date='2025-01-01')
    db.session.add(item)
    db.session.commit()
    assert 'Продажа repr' in str(item)

def test_services_repr(app_context):
    item = Services(name='Услуга repr', tovar='Т', opisan='Т', cost='1', date='2025-01-01')
    db.session.add(item)
    db.session.commit()
    assert 'Услуга repr' in str(item)


def test_tovar_kol_vo_is_string(app_context):
    tovar = Tovar(name='Кол-во', kategor='Т', proizv='Т', strana='Т', cost='1', kol_vo='999')
    db.session.add(tovar)
    db.session.commit()
    assert tovar.kol_vo == '999'

def test_prodano_cost_is_int(app_context):
    item = Prodano(name='Цена', personal='Т', cost=500, date='2025-01-01')
    db.session.add(item)
    db.session.commit()
    assert item.cost == 500

def test_services_date_is_string(app_context):
    item = Services(name='Дата', tovar='Т', opisan='Т', cost='1', date='2025-12-31')
    db.session.add(item)
    db.session.commit()
    assert item.date == '2025-12-31'

def test_no_records_initially(app_context):
    assert Tovar.query.count() == 0

def test_add_two_tovar(app_context):
    db.session.add(Tovar(name='1', kategor='Т', proizv='Т', strana='Т', cost='1', kol_vo='1'))
    db.session.add(Tovar(name='2', kategor='Т', proizv='Т', strana='Т', cost='1', kol_vo='1'))
    db.session.commit()
    assert Tovar.query.count() == 2

def test_add_two_prodano(app_context):
    db.session.add(Prodano(name='1', personal='А', cost=1, date='2025-01-01'))
    db.session.add(Prodano(name='2', personal='Б', cost=2, date='2025-01-02'))
    db.session.commit()
    assert Prodano.query.count() == 2

def test_add_two_services(app_context):
    db.session.add(Services(name='1', tovar='Т', opisan='1', cost='1', date='2025-01-01'))
    db.session.add(Services(name='2', tovar='Т', opisan='2', cost='2', date='2025-01-02'))
    db.session.commit()
    assert Services.query.count() == 2

def test_final_empty_check(app_context):
    assert db.session.query(Tovar).count() == 0  
