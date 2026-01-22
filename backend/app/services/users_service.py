from typing import Union
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateSchema
from app.core.security import get_password_hash


# Here The creation of a user and insertion into the database is managed
# This function takes in input username and hashed password of the user and creates the entity in the database
# It checks if the username is already taken
# If so it returns None, else it saves the user and returns the user object.
def create_user(db: Session, user: UserCreateSchema) -> Union[User, None]:
    existing_user = db.query(User).filter(User.nome == user.nome).first()
    if existing_user:
        return None

    hashed_password = get_password_hash(user.pswd)
    new_user = User(nome=user.nome, hashed_pswd=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

# def make_user_eat_too_much(user):
