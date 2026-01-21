from pydantic import BaseModel

class TokenResponseSchema(BaseModel):
    access_token: str  # Usiamo str perché gli ID spesso vengono trattati così nei token
    token_type: str = "bearer"
