# Import necessary modules and libraries
from flask import Blueprint, redirect, render_template, request, session, url_for
from ..queries.oauth_queries import OAuthQueries
from ..utils.verify_user_session import verify_user_session
from urllib.parse import parse_qs

# Create a Blueprint named 'home'
home = Blueprint('home', __name__)


# Route for the home page
@home.route('/')
def index():
    """
    Redirect users to the home page if logged in,
    otherwise redirect to the login page.
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
    user_session = verify_user_session()
    user_info = session.get('user_info')
    oauth_queries = OAuthQueries(user_session)

    # Query user vinyl data from Discogs API
    discogs_data = oauth_queries.query_random_vinyls()

    return render_template('home.html', user=user_info, discogs_data=discogs_data)


@home.route('/search', methods=["POST"])
def search():
    """
    Handle search requests from the user.

    Returns:
        JSON response containing the search results.
    """
    user_session = verify_user_session()
    oauth_queries = OAuthQueries(user_session)

    search_term = request.form.get("search_term")

    # Query search vinyls data from Discogs API
    discogs_data = oauth_queries.search(search_term)

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

    user_session = verify_user_session()
    user_info = session.get('user_info')
    oauth_queries = OAuthQueries(user_session)

    # Query search vinyls data from Discogs API
    response = oauth_queries.remove_collection(user_info['username'], collection_data)

    # Query user collection data from Discogs API
    discogs_data = oauth_queries.query_user_collections(user=user_info['username'])

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

    user_session = verify_user_session()
    user_info = session.get('user_info')
    oauth_queries = OAuthQueries(user_session)

    # Query search vinyls data from Discogs API
    response = oauth_queries.add_collection(user_info['username'], collection_data)

    # Query user collection data from Discogs API
    discogs_data = oauth_queries.query_user_collections(user=user_info['username'])

    return redirect(request.referrer)
