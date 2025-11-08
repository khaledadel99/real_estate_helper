# llm/parsers.py
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict
from datetime import datetime

class MessageSchema(BaseModel):
    sender: str
    intent: str
    entities: Dict[str, str] = Field(default_factory=dict)
    timestamp: Optional[datetime] = None

def validate_message(raw_json: dict) -> Optional[MessageSchema]:
    try:
        return MessageSchema(**raw_json)
    except ValidationError as e:
        print(f"⚠️ Validation failed: {e}")
        return None