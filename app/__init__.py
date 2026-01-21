from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Silakan login untuk mengakses halaman ini."

    from app.models import User
    
    @login_manager.user_loader  
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        
        from app.controllers.auth import auth_bp
        app.register_blueprint(auth_bp)

        from app.controllers.admin import admin_bp
        app.register_blueprint(admin_bp)

    return app