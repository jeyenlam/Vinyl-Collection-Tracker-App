from flask import Blueprint, current_app, redirect, render_template, session, url_for
from requests_oauthlib import OAuth1Session
from .queries.oauth_queries import OAuthQueries

views = Blueprint('views', __name__)

@views.route('/')
def index():
    user_info = session.get('user_info', None)

    if user_info is None:
        return redirect(url_for('auth.login'))

    return redirect(url_for('views.home'))


@views.route('/home')
def home():
    # Make sure that the user is logged in
    user_info = session.get('user_info', None)

    if user_info is None:
        return redirect(url_for('auth.login'))

    # Check if access_token is present in the session
    access_token = session.get('access_token', None)
    if access_token is None or 'oauth_token' not in access_token or 'oauth_token_secret' not in access_token:
        return redirect(url_for('auth.login'))
    
    discogs_oauth = OAuth1Session(
        client_key = current_app.config['DISCOGS_CONSUMER_KEY'],
        client_secret = current_app.config['DISCOGS_CONSUMER_SECRET'],
        resource_owner_key = access_token['oauth_token'],
        resource_owner_secret = access_token['oauth_token_secret'],
    )
    
    oauth_queries = OAuthQueries(discogs_oauth)

    discogs_data = oauth_queries.query_random_vinyls()
    
    current_app.logger.info(discogs_data)

    return render_template('home.html', user=user_info, discogs_data=discogs_data)
