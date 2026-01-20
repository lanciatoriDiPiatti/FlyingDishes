from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    hashed_pswd = Column(String)
    has_voted = Column(Boolean, default=False)
    fat = Column(Boolean, default=False)
