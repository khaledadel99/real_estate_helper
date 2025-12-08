# db/model.py
from sqlalchemy import Column, Float, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class units(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Float)
    region = Column(String)
    price = Column(Float)
    payment_plan = Column(String)
    apartment_type = Column(String)
    n_rooms = Column(Integer)
    insertion_date = Column(Date)
    project = Column(String)
    down_payment = Column(Integer)
    installments = Column(Integer)
    installment_value = Column(Float) 
    
    # Add a unique constraint to prevent duplicates at the database level
    __table_args__ = (
        UniqueConstraint(
            'project', 'area', 'price', 'region', 'apartment_type', 'n_rooms', 'payment_plan', 
            name='uix_unit_identity',
            postgresql_nulls_not_distinct=True
        ),
    )