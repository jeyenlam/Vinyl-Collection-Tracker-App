from flask import current_app, redirect, session, url_for
from requests_oauthlib import OAuth1Session

def verify_user_session():
  user_info = session.get('user_info')
  access_token = session.get('access_token')

  if not user_info or 'username' not in user_info:
      return redirect(url_for('auth.login'))

  if not access_token or 'oauth_token' not in access_token or 'oauth_token_secret' not in access_token:
      return redirect(url_for('auth.login'))

  # Initialize OAuth1Session with user's access token
  user_session = OAuth1Session(
      client_key=current_app.config['DISCOGS_CONSUMER_KEY'],
      client_secret=current_app.config['DISCOGS_CONSUMER_SECRET'],
      resource_owner_key=access_token['oauth_token'],
      resource_owner_secret=access_token['oauth_token_secret']
  )
  
  return user_session;
