# Import necessary modules
from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define a function to create the Flask application
def create_app():
  """
    Create and configure the Flask application instance.
    
    Returns:
      Flask: The configured Flask application instance.
  """
  # Create the Flask application instance
  app = Flask(__name__)
  
  # Configure application settings using environment variables
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  app.config['DISCOGS_CONSUMER_KEY'] = os.getenv('DISCOGS_CONSUMER_KEY')
  app.config['DISCOGS_CONSUMER_SECRET'] = os.getenv('DISCOGS_CONSUMER_SECRET')
  
  # Import blueprints for different parts of the application
  from .views import views
  from .auth import auth
  
  # Register blueprints with the Flask application instance
  app.register_blueprint(views, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')
  
  # Return the Flask application instance
  return app  