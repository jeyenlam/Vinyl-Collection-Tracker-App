from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  app.config['DISCOGS_CONSUMER_KEY'] = os.getenv('DISCOGS_CONSUMER_KEY')
  app.config['DISCOGS_CONSUMER_SECRET'] = os.getenv('DISCOGS_CONSUMER_SECRET')

  
  from .views import views
  from .auth import auth
  
  app.register_blueprint(views, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')
  
  return app  