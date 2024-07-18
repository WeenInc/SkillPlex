from .completions import Completions

class Chat:
    def __init__(self, db_url, api_key, api_base_url):
        self.completions = Completions(db_url, api_key, api_base_url)