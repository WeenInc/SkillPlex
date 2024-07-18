from .openai_client import OpenAIClient

class SkillPlex:
    def __init__(self, db_url, openai_api_key, skillplex_endpoint):
        self.openai = OpenAIClient(db_url, openai_api_key, skillplex_endpoint)