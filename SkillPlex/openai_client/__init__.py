from .openai_wrapper import OpenAIWrapper
from .chat import Chat

class OpenAIClient:
    def __init__(self, db_url, openai_api_key, skillplex_endpoint):
        self.chat = Chat(db_url, openai_api_key, skillplex_endpoint)
        self.wrapper = OpenAIWrapper(db_url, openai_api_key, skillplex_endpoint)