from .openai_wrapper import OpenAIWrapper
from .chat import Chat
import os

class OpenAIClient:
    def __init__(self, db_url=None, openai_api_key=None, skillplex_endpoint=None):
        if db_url is None:
            db_url = os.environ.get('DB_URL')  # Set a sensible default or handle it as needed
        if openai_api_key is None:
            openai_api_key = os.environ.get('OPENAI_API_KEY')
        if skillplex_endpoint is None:
            skillplex_endpoint = os.environ.get('SKILLPLEX_ENDPOINT')

        self.chat = Chat(db_url, openai_api_key, skillplex_endpoint)
        self.wrapper = OpenAIWrapper(db_url, openai_api_key, skillplex_endpoint)