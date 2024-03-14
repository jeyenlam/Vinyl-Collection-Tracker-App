# Import necessary modules and libraries
from flask import Blueprint, current_app, redirect, render_template, session, url_for
from requests_oauthlib import OAuth1Session
from .queries.oauth_queries import OAuthQueries

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Route for the entry page
@views.route('/')
def index():
    """
        Redirect users to the home page if logged in, otherwise redirect to the login page.
        
        Returns:
        - Redirects users to the login page if not logged in.
        - Redirects users to the home page if logged in.
    """
    user_info = session.get('user_info', None)

    if user_info is None:
        return redirect(url_for('auth.login'))

    return redirect(url_for('views.home'))


# Route for the home page
@views.route('/home')
def home():
    """
        Render the home page with user's vinyl data.
        
        Returns:
        - Renders the home page with user's vinyl data if logged in.
        - Redirects users to the login page if not logged in.
    """
    
    # Make sure that the user is logged in
    user_info = session.get('user_info', None)

    if user_info is None:
        return redirect(url_for('auth.login'))

    # Check if access_token is present in the session
    access_token = session.get('access_token', None)
    if access_token is None or 'oauth_token' not in access_token or 'oauth_token_secret' not in access_token:
        return redirect(url_for('auth.login'))
    
    # Initialize OAuth1Session with user's access token
    discogs_oauth = OAuth1Session(
        client_key = current_app.config['DISCOGS_CONSUMER_KEY'],
        client_secret = current_app.config['DISCOGS_CONSUMER_SECRET'],
        resource_owner_key = access_token['oauth_token'],
        resource_owner_secret = access_token['oauth_token_secret'],
    )
    
    # Initialize OAuthQueries with discogs_oauth session
    oauth_queries = OAuthQueries(discogs_oauth)

    # Query user's vinyl data from Discogs API
    discogs_data = oauth_queries.query_random_vinyls()
    
    current_app.logger.info(discogs_data)

    # Render the home page template with user's info and vinyl data
    return render_template('home.html', user=user_info, discogs_data=discogs_data)


@views.route('/profile')
def profile():
    """
        Render the user profile page with user's collection data.
        
        Returns:
        - Renders the user profile page with user's collection data if logged in.
        - Redirects users to the login page if not logged in.
    """
    
    # Make sure that the user is logged in
    user_info = session.get('user_info', None)

    if user_info is None:
        return redirect(url_for('auth.login'))

    # Check if access_token is present in the session
    access_token = session.get('access_token', None)
    if access_token is None or 'oauth_token' not in access_token or 'oauth_token_secret' not in access_token:
        return redirect(url_for('auth.login'))
    
    # Initialize OAuth1Session with user's access token
    discogs_oauth = OAuth1Session(
        client_key = current_app.config['DISCOGS_CONSUMER_KEY'],
        client_secret = current_app.config['DISCOGS_CONSUMER_SECRET'],
        resource_owner_key = access_token['oauth_token'],
        resource_owner_secret = access_token['oauth_token_secret'],
    )
    
    # Initialize OAuthQueries with discogs_oauth session
    oauth_queries = OAuthQueries(discogs_oauth)
    
    # Query user's collection data from Discogs API
    discogs_data = oauth_queries.get_user_collections(user=user_info['username'])

    current_app.logger.info(discogs_data)

    # Render the user profile page template with user's info and collection data
    return render_template('profile.html', user=user_info, discogs_data=discogs_data)
