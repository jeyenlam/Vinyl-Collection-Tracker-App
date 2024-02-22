import random


class OAuthQueries():
  
  def __init__(self, discogs_oauth = None):
    self.discogs_oauth = discogs_oauth
  
  
  def query_random_vinyls(self):
    random_vinyls_list = []
    for i in range(20):      
      url = f'https://api.discogs.com/database/search?q=&type=release&format=vinyl&sort=year&sort_order=desc&country=us,uk'
      discogs_data = self.discogs_oauth.get(url).json()
      
      if 'results' in discogs_data and discogs_data['results']:
        random_vinyl = random.randint(0, len(discogs_data['results']) - 1)
        random_vinyls_list.append(discogs_data['results'][random_vinyl])
    
    return random_vinyls_list
  
    
    