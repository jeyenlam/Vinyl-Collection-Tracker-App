import requests
import random
import time  # Import the time module for adding a delay between retries

class OAuthQueries():
  """
    Class to handle OAuth queries to the Discogs API.
  """
  
  def __init__(self, discogs_oauth=None):
    """
      Initialize OAuthQueries with a Discogs OAuth session.

      Args:
      discogs_oauth (OAuth1Session): Discogs OAuth session.
    """
    self.discogs_oauth = discogs_oauth
    self.max_retries = 20  # Define the maximum number of retries
  
  def query_random_vinyls(self):
    """
      Query random vinyl records from the Discogs database.

      Returns:
      list: List of random vinyl records.
    """
    random_vinyls_list = []
    
    for i in range(20):      
      url = f'https://api.discogs.com/database/search?q=&type=release&format=vinyl&sort=year&sort_order=desc&country=us,uk'
      retries = 0
      while retries < self.max_retries:
        try:
          discogs_data = self.discogs_oauth.get(url).json()
          break  # Break out of the retry loop if successful
        except Exception as e:
          print("Error:", e)
          retries += 1
          if retries == self.max_retries:
            print("Max retries reached. Unable to fetch data.")
            return random_vinyls_list
          print(f"Retrying... Attempt {retries}/{self.max_retries}")
          time.sleep(1)  # Add a small delay before retrying
          continue
      
      if 'results' in discogs_data and discogs_data['results']:
        random_vinyl = random.randint(0, len(discogs_data['results']) - 1)
        random_vinyls_list.append(discogs_data['results'][random_vinyl])
    
    print(discogs_data)
    return random_vinyls_list
  
  def get_user_collections(self, user):
    """
      Get user's collections from the Discogs API.

      Args:
      user (str): Discogs username.

      Returns:
      dict: User's collections.
    """
    collections = {}
    url = f'https://api.discogs.com/users/{user}/collection/folders'
    retries = 0
    
    while retries < self.max_retries:
      try:
        folders = self.discogs_oauth.get(url).json()
        print(folders)
        break  # Break out of the retry loop if successful
      except Exception as e:
        print("Error:", e)
        retries += 1
        if retries == self.max_retries:
          print("Max retries reached. Unable to fetch data.")
          return collections
        print(f"Folders: Retrying... Attempt {retries}/{self.max_retries}")
        time.sleep(2)  # Add a small delay before retrying
        continue

    for folder in folders['folders']:
      folder_id = folder['id']
      url = f'https://api.discogs.com/users/{user}/collection/folders/{folder_id}/releases'
      retries = 0
      while retries < self.max_retries:
        try:
          response = self.discogs_oauth.get(url).json()
          break  # Break out of the retry loop if successful
        except Exception as e:
          print("Error:", e)
          retries += 1
          if retries == self.max_retries:
            print("Max retries reached. Unable to fetch data.")
            continue
          print(f"Release: Retrying... Attempt {retries}/{self.max_retries}")
          time.sleep(2)  # Add a small delay before retrying
          continue
        
      name = folder['name']
      if len(response['releases']) > 0 and name != 'Uncategorized':
        collections[name] = response['releases']
    return collections