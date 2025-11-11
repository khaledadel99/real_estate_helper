# llm/parsers.py
from typing import Optional, List
from pydantic import BaseModel, ValidationError, RootModel, field_validator
from datetime import datetime, date
from db.model import units
from utils.logger import timing


def fix_date(v) -> Optional[date]:
    """Accept both dd-mm-yyyy and yyyy-mm-dd date strings."""
    if v in (None, "", "-"):
        return None
    if isinstance(v, date):
        return v
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, str):
        s = v.strip().replace("/", "-")
        s = s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))  # convert Arabic digits

        for fmt in ("%d-%m-%Y", "%Y-%m-%d"):  # 👈 allow both orders
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue

        raise ValueError(
            f"Invalid date format '{v}'. Expected format: dd-mm-yyyy or yyyy-mm-dd (e.g., 11-01-2025)"
        )

    raise ValueError(f"Invalid date type: {type(v)}")



class MessageSchema(BaseModel):
    area: float | None = None
    price: float | None = None
    region: str | None = None
    payment_plan: str | None = None
    type: str | None = None
    n_rooms: int | None = None
    insertion_date: date | None = None
    project: str | None = None
    down_payment: int | None = None
    installments: int | None = None

    @field_validator("insertion_date", mode="plain")
    def _parse_strict_date(cls, v):
        return fix_date(v)

    def to_orm(self) -> units:
        """Convert this Pydantic object into a SQLAlchemy Unit ORM object."""
        data = self.model_dump()
        return units(**data)


class MessageListSchema(RootModel[List[MessageSchema]]):
    pass


@timing
def validate_messages(raw_dict_list: list[dict]) -> list[MessageSchema]:
    try:
        validated = MessageListSchema(raw_dict_list)
        return validated.root
    except ValidationError as e:
        print(f"Validation failed for list:\n{e}\n")
        return []
