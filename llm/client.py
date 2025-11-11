from google import genai
from google.genai import types 
from dotenv import load_dotenv
import os
import json
from utils.logger import *

load_dotenv()

class LLMClient:
    """
    Wrapper around an LLM API (OpenAI, Anthropic, etc.)
    """
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        if not api_key :
            api_key = os.getenv("API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = model
        with open("config\prompt_deserialization.txt" , "r", encoding="utf-8-sig") as f :
            self.raw_deserial = f.read()
    
    @timing
    def extract_structured_data(self, text: str) -> dict:
        """
        Sends a WhatsApp message text and gets structured JSON back.
        """
        property_data = text
        response = self.client.models.generate_content(
            model=self.model,
            contents=property_data,
            config=types.GenerateContentConfig(
                system_instruction=self.raw_deserial, 
                temperature=0.0
            ),
        )
        raw_text = response.candidates[0].content.parts[0].text

        # remove the ```json ... ``` wrapper if present
        clean_json = raw_text.strip("`").replace("json", "").strip()

        # parse the JSON text into a Python dictionary
        data = json.loads(clean_json)
        return data["units"]

