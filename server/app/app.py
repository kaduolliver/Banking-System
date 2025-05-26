from flask import Flask
from dotenv import load_dotenv
import os
from routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.secret_key = os.getenv("SECRET_KEY")