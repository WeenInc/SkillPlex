import pytest
import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SkillPlex import SkillPlex

@pytest.fixture
def skillplex_instance():
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    db_url = os.environ.get('DB_URL', 'openai_history.db')
    skillplex_endpoint = os.environ.get('SKILLPLEX_ENDPOINT')
    
    print(openai_api_key, db_url, skillplex_endpoint)
    return SkillPlex(db_url, openai_api_key, skillplex_endpoint)

def test_skillplex_process_message(skillplex_instance):

    messages = [
        {"role": "system", "content": "Could search for the nearest restaurant to Le Raincy and sent the address to myemail@myemail.com?"}
    ]
    client = skillplex_instance.openai
    response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",  # Replace with the desired model
        )

    print("Chat completion response:")
    print(response)
    assert response is not None

    # If you need to get messages, you might need to adjust this part
    # depending on how the SkillPlex library handles this
    response_messages = client.chat.completions.get_messages(response.conversation_id)
    print("Response messages:")
    print(response_messages)


# Add more tests as needed