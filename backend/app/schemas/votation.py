from pydantic import BaseModel, Field

class VotationIn(BaseModel):
    votesData: list[int] = Field(default_factory=list)
    votesRistorante: list[int] = Field(default_factory=list)