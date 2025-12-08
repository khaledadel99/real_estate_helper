# insert_units.py
from db.session import SessionLocal
from sqlalchemy.dialects.postgresql import insert
from llm.parser import MessageSchema
from db.model import units
from sqlalchemy import text
from datetime import datetime, timedelta
import logging

def insert_units(orm_units: list[MessageSchema]):
    """Insert a list of SQLAlchemy ORM unit objects into the DB using a context manager."""

    # Context manager automatically handles session closing.
    with SessionLocal() as db:
        # Transaction context: auto-commit OR auto-rollback on error.
        with db.begin():
            
            data_list = []

            for u in orm_units:
                data = u.model_dump()

                # Calculate installment_value
                price = data.get('price')
                down = data.get('down_payment')
                inst = data.get('installments')

                try:
                    if price and down and inst and float(inst) > 0:
                        data['installment_value'] = round(
                            (float(price) - float(down)) / float(inst), 2
                        )
                    else:
                        data['installment_value'] = None
                except (ValueError, TypeError):
                    data['installment_value'] = None

                data_list.append(data)

            if not data_list:
                return

            stmt = insert(units).values(data_list)
            stmt = stmt.on_conflict_do_nothing(constraint='uix_unit_identity')

            result = db.execute(stmt)

        logging.info(f"Processed {len(data_list)} rows. Inserted new unique rows.")



def retrieve_units(sql_query: str, duration : int = 30):
    if not sql_query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    one_month_ago = datetime.now() - timedelta(days=duration)

    wrapped_query = f"""
        SELECT * FROM ({sql_query}) AS subquery
        WHERE subquery.insertion_date >= :min_date
    """
    print(wrapped_query)
    with SessionLocal() as db:
        result = db.execute(text(wrapped_query), {"min_date": one_month_ago})
        dict_output = [dict(r._mapping) for r in result.fetchall()]
        return dict_output