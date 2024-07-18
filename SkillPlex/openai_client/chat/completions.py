from SkillPlex.openai_client.openai_wrapper import OpenAIWrapper

class Completions:
    def __init__(self, db_url, api_key, api_base_url):
        self.wrapper = OpenAIWrapper(db_url, api_key, api_base_url)

    def create(self, messages, model="gpt-4", **kwargs):
        return self.wrapper.chat(messages, model=model, **kwargs)
    
    def get_messages(self, conversation_id):
        return self.wrapper.get_conversation_messages(conversation_id)