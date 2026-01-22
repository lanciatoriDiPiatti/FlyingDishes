from sqlalchemy import null
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.food import Food
from app.models.day import Day

def get_users_list(db: Session):
    all_users = db.query(User).all()
    return all_users


def get_all_data(db: Session):
    all_datas = db.query(Day).all()
    return all_datas


def get_all_restaurants(db: Session):
    all_restaurants = db.query(Food).all()
    return all_restaurants