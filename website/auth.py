from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from requests_oauthlib import OAuth1Session

from website import views

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  
  # Step 1. Obtain the consumer key and consumer secret from .env
  DISCOGS_CONSUMER_KEY = current_app.config['DISCOGS_CONSUMER_KEY']
  DISCOGS_CONSUMER_SECRET = current_app.config['DISCOGS_CONSUMER_SECRET']

  if request.method == 'POST':
    discogs_oauth = OAuth1Session(
      DISCOGS_CONSUMER_KEY,
      client_secret=DISCOGS_CONSUMER_SECRET,
      callback_uri=url_for('auth.callback', _external=True)
    )

    try:
      # Step 2. Send a GET request to the Discogs request token URL ¶
      request_token = discogs_oauth.fetch_request_token('https://api.discogs.com/oauth/request_token')
      
      session['request_token'] = request_token # Store the request token in the session

      # Step 3. Redirect your user to the Discogs Authorize page
      authorization_url = discogs_oauth.authorization_url('https://discogs.com/oauth/authorize?')
      return redirect(authorization_url)

    except Exception as e:
      current_app.logger.error(f'\nError during request token retrieval: {str(e)}')
      flash("Error: Failed to initiate OAuth flow", 'error')
      return redirect(url_for('auth.login'))

  return render_template('login.html')


#Call back function executed once the user grant the authorization to the app
@auth.route('/callback')
def callback():
  
  request_token = session.get('request_token')
  oauth_verifier = request.args.get('oauth_verifier')
  # current_app.logger.info(f'OAuth Verifier: {oauth_verifier}')

  if 'oauth_token' not in request_token or request_token is None or oauth_verifier is None:
    current_app.logger.info('\nOAuth Verifier or OAuth Reuqest Token Not Found')
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
    access_token = discogs_oauth.fetch_access_token('https://api.discogs.com/oauth/access_token')
    
    # Step 5. Send authenticated requests to Discogs endpoints
    user_info = discogs_oauth.get('https://api.discogs.com/oauth/identity').json() 
    current_app.logger.info(f'\nUser Info: {user_info}')  
    
    session['user_info'] = user_info # store user info in session for later use as long as logged in
    
    return redirect(url_for('views.home'))

  except Exception as e:
    current_app.logger.error(f'\nError during access token retrieval: {str(e)}')
    flash("Error: Failed to obtain access token", 'error')
    return redirect(url_for('auth.login'))
 
    
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
  # Clear user info off session
  session.clear()
  return redirect(url_for('auth.login'))