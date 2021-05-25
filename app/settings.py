import os

from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from decouple import config as env

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['DEBUG'] = env('DEBUG', cast=bool)
app.config['SECRET_KEY'] = env('SECRET_KEY', default='super-chave-nada-secreta')
app.config['MONGODB_SETTINGS'] = {
    'db': env('MONGO_INITDB_DATABASE'),
    'username': env('MONGO_INITDB_ROOT_USERNAME'),
    'password': env('MONGO_INITDB_ROOT_PASSWORD'),
    'host': env('MONGO_HOST')
}
db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)
