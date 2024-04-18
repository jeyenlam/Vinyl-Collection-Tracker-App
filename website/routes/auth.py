from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from requests_oauthlib import OAuth1Session

# Create a Blueprint named 'auth'
auth = Blueprint('auth', __name__)

# Define the URLs for Discogs OAuth flow
request_token_url = "https://api.discogs.com/oauth/request_token"
authorize_url = "https://www.discogs.com/oauth/authorize"
access_token_url = "https://api.discogs.com/oauth/access_token"


# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login using Discogs OAuth authentication.

    Returns:
        - GET: Renders the login page.
        - POST: Initiates the OAuth flow and
        redirects the user to Discogs for authorization.
    """
    # Step 1. Obtain the consumer key and consumer secret from .env
    discogs_oauth = OAuth1Session(
        client_key=current_app.config['DISCOGS_CONSUMER_KEY'],
        client_secret=current_app.config['DISCOGS_CONSUMER_SECRET'],
        callback_uri=url_for('auth.callback', _external=True)
    )

    if request.method == 'POST':
        try:
            # Step 2. Send a GET request to the Discogs request token URL
            request_token = discogs_oauth.fetch_request_token(request_token_url)
            session['request_token'] = request_token

            # Step 3. Redirect your user to the Discogs Authorize page
            return redirect(discogs_oauth.authorization_url(authorize_url))

        except Exception as e:
            current_app.logger.error(f'\nRequest Token Error: {str(e)}')
            flash("Error: Failed to initiate OAuth flow", 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/callback')
def callback():
    """
    Handle OAuth callback from Discogs after user authorization.

    Returns:
        - Redirects the user to the home page upon successful authentication.
    """
    request_token = session.get('request_token')
    oauth_verifier = request.args.get('oauth_verifier')

    if (
        'oauth_token' not in request_token
        or request_token is None
        or oauth_verifier is None
    ):
        current_app.logger.info('\nOAuth Verifier or Request Token Not Found')
        return redirect(url_for('auth.login'))

    try:
        # Use the OAuth1Session to get the access token
        discogs_oauth = OAuth1Session(
            current_app.config['DISCOGS_CONSUMER_KEY'],
            client_secret=current_app.config['DISCOGS_CONSUMER_SECRET'],
            resource_owner_key=request_token['oauth_token'],
            resource_owner_secret=request_token['oauth_token_secret'],
            verifier=oauth_verifier
        )

        # Step 4. Send a POST request to the Discogs access token URL
        access_token = discogs_oauth.fetch_access_token(access_token_url)
        session['access_token'] = access_token

        # Step 5. Send authenticated requests to Discogs endpoints
        user_info = discogs_oauth.get('https://api.discogs.com/oauth/identity').json()
        session['user_info'] = user_info

        return redirect(url_for('home.display_home'))

    except Exception as e:
        current_app.logger.error(f'\nToken Retrieval Error: {str(e)}')
        flash("Error: Failed to obtain access token", 'error')
        return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Handle user logout by clearing the session data.

    Returns:
        - Redirects the user to the login page after logout.
    """
    session.clear()
    return redirect(url_for('auth.login'))
