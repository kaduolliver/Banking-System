import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.cliente_routes import cliente_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "chave_fallback_insegura") 
    
    # Ajuste o origin para o domínio/porta do seu frontend React
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    return app
