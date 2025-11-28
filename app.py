from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main_bp
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_page'

    # Registrar Blueprint
    app.register_blueprint(main_bp)

    # User Loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Crear tablas (en desarrollo)
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
