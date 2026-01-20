from pydantic import BaseModel, Field

class VotationIn(BaseModel):
    Data: list[int] = Field(default_factory=list)
    Ristoranti: list[int] = Field(default_factory=list)