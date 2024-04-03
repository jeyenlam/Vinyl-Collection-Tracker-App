# Import necessary modules and libraries
from flask import Blueprint, current_app, render_template, session
from ..queries.oauth_queries import OAuthQueries
from ..utils.verify_user_session import verify_user_session

# Create a Blueprint named 'home'
home = Blueprint('home', __name__)

# Route for the home page
@home.route('/')
@home.route('/home')
def index():
    """
    Render the home page with user's vinyl data if logged in,
    otherwise redirect to the login page.
    """
    
    user_session = verify_user_session() #return user session if verified else redirect to login
    user_info = session.get('user_info') #get user info for rendering pages

    # Initialize OAuthQueries with discogs_oauth session
    oauth_queries = OAuthQueries(user_session)

    # Query user's vinyl data from Discogs API
    discogs_data = oauth_queries.query_random_vinyls()
    
    current_app.logger.info(discogs_data)

    # Render the home page template with user's info and vinyl data
    return render_template('home.html', user=user_info, discogs_data=discogs_data)