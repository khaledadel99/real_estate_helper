from fastapi import FastAPI
from llm.client import LLMClient
from llm.parser import validate_messages
from db.units_db import insert_units, retrieve_units
import json

app = FastAPI()
llm = LLMClient()


@app.post("/scrape")
def scrape_data():
    try:
        from scraping.whatsapp_scraper import main_scraping
        
        raw_data = main_scraping()
        structured = llm.extract_structured_data(raw_data)
        validated = validate_messages(structured)
        insert_units(validated)

        return {
            "status": "success",
            "inserted_records": len(validated)
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/ask")
def ask_question(question: str):
    try:
        query = llm.generate_query(question)
        units = retrieve_units(query, duration=300)
        final_answer = llm.convert_output(units)

        return {
            "sql_query": query,
            "units_found": len(units),
            "answer": final_answer
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
