# controllers/votation_controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.votation import VotationIn
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.votation_service import submit_votation
from app.services.votation_service import get_current_avgs

router = APIRouter()


# API post endpoint fot the votation:
# We want in input a json containing 2 fields: Data array of ints and Ristornati array of ints
# We will extract the two arrays and call different functions that:
# - Retrieves the id of the voter from the auth token
# - Update the votes arrays of the Day and Food models
# - Recalculate the current_avg fields for both models
@router.post("/votation", status_code=status.HTTP_201_CREATED)
def create_votation(
    payload: VotationIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db = db
    day_votes=payload.votesData
    food_votes=payload.votesRistorante
    print(day_votes)
    print(food_votes)
    # current_user.id è il voter id (estratto dal token nella dependency)
    submit_votation(
        db,
        voter_id=current_user.id,
        day_votes = day_votes,
        food_votes = food_votes,
    )
    return {"ok": True}


@router.get("/standigs",status_code=status.HTTP_200_OK)
def get_current_results(db: Session = Depends(get_db)):
    current_avgs = get_current_avgs(db)
    return current_avgs