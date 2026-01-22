from pydantic import BaseModel, Field

class VotationIn(BaseModel):
    votesRistorante: list[int] = Field(default_factory=list)
    votesData: list[int] = Field(default_factory=list)