from flask import Blueprint, render_template, session

views = Blueprint('views', __name__)

@views.route('/')
def index():
  return render_template('home.html')

@views.route('/home')
def home():
  user_info = session.get('user_info', None)
  
  if user_info is None:
    return render_template('home.html')
  
  return render_template('home.html', user=user_info)