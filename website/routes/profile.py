# Import necessary modules and libraries
from flask import Blueprint, current_app, render_template, session
from ..queries.oauth_queries import OAuthQueries
from ..utils.verify_user_session import verify_user_session

# Create a Blueprint named 'home'
profile = Blueprint('profile', __name__)

# Route for the user profile page (commented out)
@profile.route('/profile')
def index():
    """
    Render the user profile page with user's collection data if logged in,
    otherwise redirect to the login page.
    """
    
    user_session = verify_user_session() #return user session if verified else redirect to login
    user_info = session.get('user_info') #get user info for rendering pages

    # Initialize OAuthQueries with discogs_oauth session
    oauth_queries = OAuthQueries(user_session)

    # Query user's collection data from Discogs API
    discogs_data = oauth_queries.get_user_collections(user=user_info['username'])

    current_app.logger.info(discogs_data)

    # Render the user profile page template with user's info and collection data
    return render_template('profile.html', user=user_info, discogs_data=discogs_data)
