# controllers/votation_controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Any, Dict

from app.db.session import get_db
from app.schemas.votation import VotationIn
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.votation_service import submit_votation
from app.services.votation_service import get_current_avgs
from app.services.votation_service import final_choice_days, final_choice_foods


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
    print(payload)
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


@router.get("/standings",status_code=status.HTTP_200_OK)
def get_current_results(db: Session = Depends(get_db)):
    current_avgs = get_current_avgs(db)
    print(f"{current_avgs}")
    return current_avgs


@router.post("/yavc", status_code= status.HTTP_200_OK )
def debug_votation(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    # Estrazione manuale dei dati
    day_votes = payload.get("votesData", [])
    food_votes = payload.get("votesRistorante", [])
    current_user_id = current_user.id
    
    # Debug print
    print(f"DEBUG - Day Votes: {day_votes}")
    print(f"DEBUG - Food Votes: {food_votes}")
    print(f"DEBUG - user: {current_user_id}")

    submit_votation(
        db,
        current_user_id,
        day_votes,
        food_votes
    )

@router.get("/final_choice", status_code=status.HTTP_200_OK)
def get_final_choice(db: Session = Depends(get_db)):
    day_winner = final_choice_days(db)
    food_winner = final_choice_foods(db)
    return {"data-vincitore": day_winner,"ristorante-vincitore": food_winner}
