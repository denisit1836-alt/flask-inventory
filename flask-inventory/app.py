from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


from controllers.tovar_controller import bp as tovar_bp
from controllers.prodano_controller import bp as prodano_bp
from controllers.services_controller import bp as services_bp
from controllers.auth_controller import bp as auth_bp


from models.tables import db
from models.user import User, UserRepo

app = Flask(__name__, template_folder="views", static_folder="static")


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:123456789@localhost/flask_db'
app.config['SECRET_KEY'] = 'your_very_strong_secret_key_here_change_it!'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Пожалуйста, войдите в систему."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(tovar_bp)
app.register_blueprint(prodano_bp)
app.register_blueprint(services_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))


with app.app_context():
    db.create_all()
    repo = UserRepo()
    if not repo.get_by_username('admin'):
        repo.add('admin', 'password123')
        print("Создан администратор: admin / password123")

if __name__ == "__main__":
    app.run(debug=True)
