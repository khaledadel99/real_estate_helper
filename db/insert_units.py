# insert_units.py
from db.session import SessionLocal
from sqlalchemy.dialects.postgresql import insert
from llm.parser import MessageSchema
from db.model import units
import logging
from sqlalchemy import text


def insert_units(orm_units: list[MessageSchema]):
    """Insert a list of SQLAlchemy ORM unit objects into the DB."""
    db = SessionLocal()
    try:
        # Step 1️⃣ — Insert all rows (no conflict check)
        stmt = insert(units).values([u.model_dump() for u in orm_units])
        db.execute(stmt)
        db.commit()
        # Step 2️⃣ — Remove duplicates (keep the first row per unique combination)
        dedup_query = text("""
            DELETE FROM units a
            USING units b
            WHERE a.id > b.id
              AND a.area IS NOT DISTINCT FROM b.area
              AND a.price IS NOT DISTINCT FROM b.price
              AND a.payment_plan IS NOT DISTINCT FROM b.payment_plan
              AND a.type IS NOT DISTINCT FROM b.type
              AND a.n_rooms IS NOT DISTINCT FROM b.n_rooms
              AND a.project IS NOT DISTINCT FROM b.project
              AND a.down_payment IS NOT DISTINCT FROM b.down_payment
              AND a.installments IS NOT DISTINCT FROM b.installments       
              AND a.region IS NOT DISTINCT FROM b.region                                
            ;
        """)
        db.execute(dedup_query)
        db.commit()     

        update_query = text("""
            UPDATE units
            SET installment_value = ROUND((price - down_payment) / installments)
            WHERE price IS NOT NULL AND down_payment IS NOT NULL;
        """)
        db.execute(update_query)
        db.commit()
     
        logging.info(f"Inserted {len(orm_units)} rows into 'units' table.")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inserting units: {e}")
    finally:
        db.close()