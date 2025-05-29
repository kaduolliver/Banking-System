import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.routes.auth_routes import auth_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "chave_fallback_insegura") 
    CORS(app, supports_credentials=True)
    app.register_blueprint(auth_bp)
    return app