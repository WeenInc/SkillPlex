from datetime import datetime
import os
from SkillPlex.database import initialize_db
from SkillPlex.tools.object_tools import get_attribute_or_key
from openai import OpenAI

import sqlite3
import uuid
import json
import logging
from SkillPlex.external_executor import ExternalAPIExecutor
from SkillPlex.skills_selector import SkillPlexToolsSelector

class OpenAIWrapper:
    def __init__(self, db_url, openai_api_key, skillplex_endpoint):
        initialize_db(db_url)
        self.client = OpenAI(api_key=openai_api_key)
        self.conn = sqlite3.connect(db_url, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.api_executor = ExternalAPIExecutor(skillplex_endpoint)
        self.skills_selector = SkillPlexToolsSelector()

    def create_conversation(self):
        conversation_id = str(uuid.uuid4())
        self.cur.execute('INSERT INTO conversations (conversation_id) VALUES (?)', (conversation_id,))
        self.conn.commit()
        return conversation_id

    def get_conversation_id(self, conversation_id):
        self.cur.execute('SELECT id FROM conversations WHERE conversation_id = ?', (conversation_id,))
        row = self.cur.fetchone()
        return row[0] if row else None

    def store_message(self, conversation_id, message):
        conversation_db_id = self.get_conversation_id(conversation_id)
        if conversation_db_id:
            self.cur.execute('INSERT INTO messages (conversation_id, message) VALUES (?, ?)', 
                             (conversation_db_id, message))
            self.conn.commit()

    def executeSkill(self, skillName, skillDescription, skillArgs):
        return self.api_executor.execute(skillName, skillDescription, skillArgs)

    def chat(self, messages, model="gpt-4", **kwargs):
        if 'conversation_id' in kwargs:
            conversation_id = kwargs['conversation_id']
            del kwargs['conversation_id']
        else:
            conversation_id = self.create_conversation()

        try:
            for message in messages:
                self.store_message(conversation_id, json.dumps(message))

            history_messages = self.get_conversation_messages(conversation_id)

            response = self.client.chat.completions.create(
                model=model,
                messages=self.set_technical_context(history_messages),
                tools=self.skills_selector.get_tools(),
                **kwargs)
            
            usage = response.usage

            response_message = response.choices[0].message

            self.store_message(conversation_id, json.dumps(self.transform_to_serializable_message(response_message)))

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    logging.info(tool_call)

                    skillName = tool_call.function.name
                    skillArgs = json.loads(tool_call.function.arguments)

                    skillResult = self.executeSkill(skillName, "", skillArgs)

                    if skillResult["type"] == 'synchronous':
                        response = self.process_tool_result(conversation_id, tool_call.id, skillName, skillResult["result"], model=model, **kwargs)
                        if 'usage' in response:
                            usage["completion_tokens"] += response.usage.completion_tokens
                            usage["prompt_tokens"] += response.usage.prompt_tokens
                            usage["total_tokens"] += response.usage.total_tokens
                            response.usage = usage
                    else:
                        raise Exception("Asynchronous results are not yet supported")

            if isinstance(response, dict):
                response['conversation_id'] = conversation_id
            else:
                setattr(response, 'conversation_id', conversation_id)
                return response

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    import json

    def transform_to_serializable_message(self, response_message):
        # Check if response_message is an instance of ChatCompletionMessage
        role = get_attribute_or_key(response_message, 'role')
        content = get_attribute_or_key(response_message, 'content')
        tool_calls = self.serialize_tool_calls(get_attribute_or_key(response_message, 'tool_calls'))
        tool_call_id = get_attribute_or_key(response_message, 'tool_call_id')
        
        # Serialize the response message
        if tool_calls:
            return {
                "role": role,
                "content": content,
                "tool_calls": tool_calls
            }
        elif tool_call_id:
            {
                "role": role,
                "content": content,
                "tool_call_id": tool_call_id
            }
        else:
            return {
                "role": role,
                "content": content
            }
    
    def transform_to_serializable_messages(self, response_messages):
        serialized_response_messages = []
        for response_message in response_messages:
            serialized_response_messages.append(self.transform_to_serializable_message(response_message))
        return serialized_response_messages

    def serialize_tool_calls(self, tool_calls):
        if not tool_calls:
            return None
        
        serialized_tool_calls = []
        for tool_call in tool_calls:
            if hasattr(tool_call, 'function'):
                arguments = tool_call.function.arguments
                name = tool_call.function.name
                id = tool_call.id
                type = tool_call.type
            else:
                arguments = tool_call.get('function').get('arguments')
                name = tool_call.get('function').get('name')
                id = tool_call.get('id')
                type = tool_call.get('type')

            serialized_tool_calls.append({
                "function": {
                    "arguments": arguments,
                    "name": name
                },
                "id": id,
                "type": type
            })
        return serialized_tool_calls
    
    def is_all_tool_calls_answered(self, messages):
        tool_call_ids = set()
        tool_response_ids = set()

        for message in messages:
            if message['role'] == 'assistant' and 'tool_calls' in message:
                for tool_call in message['tool_calls']:
                    tool_call_ids.add(tool_call['id'])
            elif message['role'] == 'tool' and 'tool_call_id' in message:
                tool_response_ids.add(message['tool_call_id'])

        return tool_call_ids == tool_response_ids

    def process_tool_result(self, conversation_id, tool_call_id, tool_name, tool_result, model="gpt-4", **kwargs):
        try:
            messages = self.get_conversation_messages(conversation_id)
            tool_message = {
                "role": "tool",
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(tool_result)
                    }
                ],
                "tool_call_id": tool_call_id
            }
            self.store_message(conversation_id, json.dumps(tool_message))
            messages.append(tool_message)

            if not self.is_all_tool_calls_answered(messages):
                return messages

            response = self.client.chat.completions.create(
                model=model,
                messages=self.set_technical_context(messages),
                tools=self.skills_selector.get_tools(),
                **kwargs)
            usage = response.usage

            response_message = response.choices[0].message

            self.store_message(conversation_id, json.dumps(self.transform_to_serializable_message(response_message)))

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    logging.info(tool_call)

                    skillName = tool_call.function.name
                    skillArgs = json.loads(tool_call.function.arguments)

                    skillResult = self.executeSkill(skillName, "", skillArgs)

                    if skillResult["type"] == 'synchronous':
                        response = self.process_tool_result(conversation_id, tool_call.id, skillName, skillResult["result"], model=model, **kwargs)
                        if 'usage' in response:
                            usage["completion_tokens"] += response.usage.completion_tokens
                            usage["prompt_tokens"] += response.usage.prompt_tokens
                            usage["total_tokens"] += response.usage.total_tokens
                            response.usage = usage
                    else:
                        raise Exception("Asynchronous results are not yet supported")

            return response
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def get_conversation_messages(self, conversation_id):
        conversation_db_id = self.get_conversation_id(conversation_id)
        self.cur.execute('SELECT message FROM messages WHERE conversation_id = ? ORDER BY id ASC', (conversation_db_id,))
        rows = self.cur.fetchall()
        messages = []
        for row in rows:
            message = json.loads(row[0])
            messages.append(message)
        return messages

    def set_technical_context(self, messages):
        technical_context = f"""---\nTechnical Context\n---\n
        Current DateTime: {datetime.now()}\n
        ---\n"""
        if messages and messages[0]['role'] == 'system':
            messages[0]['content'] = f"\n\n{technical_context}" + messages[0]['content']
        else:
            messages.insert(0, {"role": "system", "content": technical_context})
        return messages

    def close(self):
        self.conn.close()