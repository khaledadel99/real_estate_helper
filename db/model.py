# db/model.py
from sqlalchemy import Column, Float, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class units(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Float)
    price = Column(Float)
    payment_plan = Column(String)
    type = Column(String)
    n_rooms = Column(Integer)
    insertion_date = Column(Date)
    project = Column(String)
    down_payment = Column(Integer)
    installments = Column(Integer)
    