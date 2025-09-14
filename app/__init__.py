from flask import Flask
from flask_jwt_extended import JWTManager
from .models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chatbot'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lightusers.db'
    app.config['JWT_SECRET_KEY'] = 'shubham'

    db.init_app(app)
    JWTManager(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    from .routes.auth import user_bp
    from .routes.chat import chat_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    return app
