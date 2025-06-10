import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.client_routes import client_bp
from app.routes.user_routes import user_bp
from app.routes.employee_routes import employee_bp
from app.routes.agency_routes import agency_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "chave_fallback_insegura") 
    
    app.config['DEBUG'] = True

    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(agency_bp)

    return app
