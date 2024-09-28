import requests
import logging

class ExternalAPIExecutor:
    def __init__(self, skillplex_endpoint):
        self.skillplex_endpoint = skillplex_endpoint

    def execute(self, skillName, skillDescription, skillArgs):
        try:
            response = requests.post(
                f"{self.skillplex_endpoint}",
                json={
                    "name": skillName,
                    "description": skillDescription,
                    "properties": skillArgs
                }
            )
            response.raise_for_status()
            result = response.json()

            if result.get("status") == "pending":
                return {"type": "asynchronous", "status": "pending"}
            else:
                return {"type": "synchronous", "result": result.get("result"), "status": "success"}

        except requests.RequestException as e:
            logging.error(f"An error occurred while calling SkillPlex API: {e}")
            return {"type": "error", "message": str(e)}