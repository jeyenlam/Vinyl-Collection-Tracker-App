import random

class OAuthQueries():
  """
    Class to handle OAuth queries to the Discogs API.
  """
  
  def __init__(self, user_session = None):
    self.user_session = user_session
  
  def query_random_vinyls(self):
    """
      Query random vinyl records from the Discogs database.
      Returns:
        list: List of random vinyl records.
    """
    random_vinyls_list = []
    url = 'https://api.discogs.com/database/search?q=&type=release&format=vinyl&sort=year&sort_order=desc&country=us,uk'
    
    try:
      discogs_data = self.user_session.get(url).json()
    except Exception as e:
        print("Error:", e)
    
    if 'results' in discogs_data and discogs_data['results']:
      random.shuffle(discogs_data['results']) # Shuffle the results to randomize the order
      random_vinyls_list = discogs_data['results'][:20] # Take the first 20 items from the shuffled results

    # print(random_vinyls_list)
    return random_vinyls_list
  
  def query_user_collections(self, user):
    """
      Get user's collections from the Discogs API.
      Args:
        user (str): Discogs username.
      Returns:
        dict: User's collections.
    """
    collections = {}
    url = f'https://api.discogs.com/users/{user}/collection/folders'
    
    try:
      folders = self.user_session.get(url).json()
    except Exception as e:
      print("Error:", e)

    for folder in folders['folders']:
      folder_id = folder['id']
      name = folder['name']
      url = f'https://api.discogs.com/users/{user}/collection/folders/{folder_id}/releases'

      try:
        response = self.user_session.get(url).json()
      except Exception as e:
        print("Error:", e)
        
      if len(response['releases']) > 0 and name != 'Uncategorized':
        collections[name] = response['releases']
        
    return collections
  
  def search(self, search_term):
    search_vinyls_list = []
    url = f'https://api.discogs.com/database/search?q={search_term}'
    
    try:
      discogs_data = self.user_session.get(url).json()
    except Exception as e:
        print("Error:", e)
        
    if 'results' in discogs_data and discogs_data['results']:
      search_vinyls_list = discogs_data['results'][:20] # Take the first 20 items from the shuffled results
    
    print(search_vinyls_list)
    
    return search_vinyls_list
    