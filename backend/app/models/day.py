from typing import List
from sqlalchemy import Column, Integer, String, ARRAY
from app.db.base import Base
from sqlalchemy import Float


class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    votes = Column(ARRAY(Integer), default=[])
    current_avg = Column(Float, default=0.0)
    current_var = Column(Float, default = 0.0)
