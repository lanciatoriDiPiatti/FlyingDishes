# All necessary imports
from typing import Union
from app.models.user import User
from app.core.security import verify_password
from sqlalchemy.orm import Session

# Here there are functions realted to authentication



# This function checks whether the provided username and password are valid
# It returns True for correct credentials, False otherwise
def check_authentication(db: Session, nome: str, pswd: str) -> Union[User, None]:
    user = db.query(User).filter(User.nome == nome).first()
    if not user or not verify_password(pswd, user.hashed_pswd):
        return None
    return user