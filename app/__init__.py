from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.routes import main
app.register_blueprint(main)

def create_app(config_class=Config):
    return app
