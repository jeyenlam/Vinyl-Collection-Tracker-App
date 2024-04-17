# Import necessary modules and libraries
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from ..queries.oauth_queries import OAuthQueries
from ..utils.verify_user_session import verify_user_session
from urllib.parse import urlparse, parse_qs
import json

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
    """
    Handle search requests from the user.

    Returns:
        json: JSON response containing the search results.
    """
    request_data = request.form.get("search_term") # extract request data from POST request body
    print(request_data)
    
    user_session = verify_user_session() #return user session if verified, else redirect to login
    oauth_queries = OAuthQueries(user_session) #initialize OAuthQueries

    search_term = request_data
    discogs_data = oauth_queries.search(search_term) #query search vinyls data from Discogs API
    
    # return updated discog_data
    return discogs_data


@home.route('/remove-from-collection')
def remove_from_collection():
    """
    Remove a vinyl from the user's collection.

    Returns:
        Redirects to the previous page.
    """
    # Extract the query string from the URL
    query_string = request.query_string.decode("utf-8")
    
    # Parse the query string to get the collection data
    query_params = parse_qs(query_string)

    collection_data = {
        "folder_id": query_params.get("folder", [""])[0],
        "release_id": query_params.get("release", [""])[0],
        "instance_id": query_params.get("instance", [""])[0]
    }
    print(collection_data)

    user_session = verify_user_session()  # return user session if verified, else redirect to login
    user_info = session.get('user_info') #get user info for rendering pages
    oauth_queries = OAuthQueries(user_session)  # initialize OAuthQueries

    response = oauth_queries.remove_collection(user_info['username'], collection_data)  # query search vinyls data from Discogs API

    print(response)

    discogs_data = oauth_queries.query_user_collections(user=user_info['username']) #query user collection data from Discogs API

    # Render the user profile page template with user's info and collection data
    return redirect(request.referrer)


@home.route('/add-to-collection')
def add_to_collection():
    """
    Add a vinyl to the user's collection.

    Returns:
        Redirects to the previous page.
    """
    # Extract the query string from the URL
    query_string = request.query_string.decode("utf-8")
    
    # Parse the query string to get the collection data
    query_params = parse_qs(query_string)

    collection_data = {
        "folder_id": query_params.get("folder", [""])[0],
        "release_id": query_params.get("release", [""])[0]
    }
    print(collection_data)

    user_session = verify_user_session()  # return user session if verified, else redirect to login
    user_info = session.get('user_info') #get user info for rendering pages
    oauth_queries = OAuthQueries(user_session)  # initialize OAuthQueries

    response = oauth_queries.add_collection(user_info['username'], collection_data)  # query search vinyls data from Discogs API

    print(response)

    discogs_data = oauth_queries.query_user_collections(user=user_info['username']) #query user collection data from Discogs API

    # Render the user profile page template with user's info and collection data
    return redirect(request.referrer)
    