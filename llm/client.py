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

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_DIR = os.path.join(BASE_DIR, "..", "config") 
        prompt_deserialization = os.path.join(CONFIG_DIR, "prompt_deserialization.txt")
        prompt_generate_query = os.path.join(CONFIG_DIR, "prompt_generate_query.txt")
        prompt_convert_output = os.path.join(CONFIG_DIR, "prompt_convert_output.txt")



        with open(prompt_deserialization, "r", encoding="utf-8-sig") as f :
            self.prompt_extracting = f.read()

        with open(prompt_generate_query, "r", encoding="utf-8-sig") as f :
            self.prompt_query = f.read()
        
        with open(prompt_convert_output, "r", encoding="utf-8-sig") as f :
            self.prompt_convert_output = f.read()

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
                system_instruction=self.prompt_extracting, 
                temperature=0.0
            ),
        )
        raw_text = response.candidates[0].content.parts[0].text

        # remove the ```json ... ``` wrapper if present
        clean_json = raw_text.strip("`").replace("json", "").strip()

        # parse the JSON text into a Python dictionary
        data = json.loads(clean_json)
        return data
    
    @timing
    def generate_query(self, text: str) -> dict:
        """
        Generate a valid query based on free text input.
        """
        property_data = text
        response = self.client.models.generate_content(
            model=self.model,
            contents=property_data,
            config=types.GenerateContentConfig(
                system_instruction=self.prompt_query, 
                temperature=0.0
            ),
        )
        query = response.candidates[0].content.parts[0].text

        # remove the ```json ... ``` wrapper if present
        return query
    
    @timing
    def convert_output(self, text: list[dict]) -> str:
        """
        Convert a list of units into a friendly Arabic text.
        """
        cleaned = []
        for unit in text:
            unit_copy = unit.copy()
            unit_copy.pop("insertion_date", None)  # remove safely if exists
            cleaned.append(unit_copy)
            
        property_data = json.dumps(cleaned)
        response = self.client.models.generate_content(
            model=self.model,
            contents=property_data,
            config=types.GenerateContentConfig(
                system_instruction=self.prompt_convert_output, 
                temperature=0.0
            ),
        )
        text = response.candidates[0].content.parts[0].text

        # remove the ```json ... ``` wrapper if present
        return text

