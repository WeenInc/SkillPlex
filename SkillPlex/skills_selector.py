tools = [
    {
        "type": "function",
        "function": {
            "name": "scheduleFunction",
            "description": "Function that schedules a series of actions to perform at a specified time or interval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "actions": {
                        "type": "array",
                        "description": "An array of action objects, each containing a description of the action, the arguments necessary to perform the action, and the index at which the action should be performed.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "actionDescription": {
                                    "type": "string",
                                    "description": "The description of the action to be performed."
                                },
                                "actionArgs": {
                                    "type": "object",
                                    "description": "The arguments necessary to perform the action."
                                },
                                "index": {
                                    "type": "integer",
                                    "description": "The index at which the action should be performed relative to other actions."
                                }
                            },
                            "required": ["actionDescription", "actionArgs", "index"]
                        }
                    },
                    "interval": {
                        "type": "object",
                        "description": "The interval at which to re-send the email.",
                        "properties": {
                            "count": {
                                "type": "integer",
                                "description": "The number of units for the interval."
                            },
                            "unit": {
                                "type": "string",
                                "description": "The unit of time for the interval (e.g., 'Second', 'Minute', 'Hour', 'Day', 'Week', 'Month')."
                            }
                        },
                        "required": ["count", "unit"]
                    },
                    "processAt": {
                        "type": "string",
                        "format": "date-time",
                        "description": "The UTC datetime at which to send the email."
                    }
                },
                "required": ["actions", "processAt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "searchNotion",
            "description": "Search for a specific query inside a Notion workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look for inside the Notion workspace."
                    },
                    "workspaceId": {
                        "type": "string",
                        "description": "The ID of the Notion workspace to search in."
                    }
                },
                "required": ["query", "workspaceId"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "searchNotionDatabase",
            "description": "Search for a database inside a Notion workspace by name or description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "databaseName": {
                        "type": "string",
                        "description": "The name of the database to search for."
                    },
                    "databaseDescription": {
                        "type": "string",
                        "description": "The description of the database to search for."
                    },
                    "workspaceId": {
                        "type": "string",
                        "description": "The ID of the Notion workspace to search in."
                    }
                },
                "required": ["workspaceId"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "insertNotionDatabaseItem",
            "description": "Insert a new item into a Notion database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "databaseId": {
                        "type": "string",
                        "description": "The ID of the Notion database to insert the item into."
                    },
                    "itemProperties": {
                        "type": "object",
                        "description": "The properties of the item to insert."
                    }
                },
                "required": ["databaseId", "itemProperties"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "googleSearch",
            "description": "Perform a Google search for a specified query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look for on Google."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sendEmail",
            "description": "Send an email to a specified recipient with a subject and message body.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "The email address of the recipient."
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email."
                    },
                    "body": {
                        "type": "string",
                        "description": "The body content of the email."
                    }
                },
                "required": ["recipient", "subject", "body"]
            }
        }
    }
]

class SkillPlexToolsSelector:
    def __init__(self):
        self.tools = tools

    def get_tools(self):
        return self.tools