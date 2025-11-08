from llm.client import LLMClient

class QueryAssistant:
    """
    Uses Gemini to translate user input into SQL queries
    matching your database schema.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_sql(self, user_input: str) -> str:
        system_prompt = (
            "You are a SQL expert. "
            "The database table is called 'messages' and has columns: "
            "id, sender, intent, entities, timestamp. "
            "Convert user input into a valid SQL SELECT query."
        )
        prompt = f'User request: "{user_input}". Return only the SQL query.'
        sql = self.llm.ask(prompt, system_instruction=system_prompt)
        return sql.strip()