# Import necessary modules and libraries
from flask import Blueprint, render_template, session
from website.queries.oauth_queries import OAuthQueries
from website.utils.verify_user_session import verify_user_session

# Create a Blueprint named 'home'
profile = Blueprint('profile', __name__)


# Route for the user profile page (commented out)
@profile.route('/profile')
def index():
    """
    Render the user profile page with user's collection data if logged in,
    otherwise redirect to the login page.
    """

    user_session = verify_user_session()
    user_info = session.get('user_info')

    oauth_queries = OAuthQueries(user_session)

    # Extract the username from user_info
    username = user_info['username']

    # Query user collection data from Discogs API
    discogs_data = oauth_queries.query_user_collections(user=username)

    # Render the user profile page with user's info and collection data
    return render_template('profile.html', user=user_info, discogs_data=discogs_data)
