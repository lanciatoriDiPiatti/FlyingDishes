# Here there are all the functions called by the controllers


from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateSchema
from app.core.security import get_password_hash


# Here The creation of a user and insertion into the database is managed
# This function takes in input username and hashed password of the user and creates the entity in the database
# It checks if the username is already taken
# If so it returns False, else it saves the user and returns True
# It returns true if the user has been created successfully, false otherwise

def create_user(db: Session, user: UserCreateSchema) -> bool:
    existing_user = db.query(User).filter(User.nome == user.nome).first()
    if existing_user:
        return False

    hashed_password = get_password_hash(user.pswd)
    new_user = User(nome=user.nome, hashed_pswd=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True
    

