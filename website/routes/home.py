# Import necessary modules and libraries
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from ..queries.oauth_queries import OAuthQueries
from ..utils.verify_user_session import verify_user_session
from urllib.parse import parse_qs

# Create a Blueprint named 'home'
home = Blueprint('home', __name__)

# Route for the home page
@home.route('/')
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

    return redirect(url_for('home.display_home'))
    
    
@home.route('/home')
def display_home():
    """
    Render the home page with user's vinyl data if logged in,
    otherwise redirect to the login page.
    """
    
    user_session = verify_user_session() #return user session if verified, else redirect to login
    user_info = session.get('user_info') #get user info for rendering pages
    
    oauth_queries = OAuthQueries(user_session) #initialize OAuthQueries

    discogs_data = oauth_queries.query_random_vinyls() #query user vinyl data from Discogs API
    
    # current_app.logger.info(discogs_data)
    # render the home page
    return render_template('home.html', user=user_info, discogs_data = discogs_data)


@home.route('/search', methods=["POST"])
def search():
    request_data = request.form.get("search_term") # extract request data from POST request body
    print(request_data)
    # decoded_request_data = request_data.decode('utf-8') # decode data
    # parsed_data = parse_qs(decoded_request_data) # parse data

    # search_term = parsed_data.get('search_term', [None])[0]
    # print(search_term)
    
    user_session = verify_user_session() #return user session if verified, else redirect to login
    oauth_queries = OAuthQueries(user_session) #initialize OAuthQueries

    search_term = request_data
    discogs_data = oauth_queries.search(search_term) #query search vinyls data from Discogs API
    
    # return updated discog_data
    return discogs_data
