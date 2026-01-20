from pydantic import BaseModel

class UserAuth(BaseModel):
    nome: str
    pswd: str

class UserCreateSchema(BaseModel):
    nome: str
    pswd: str
