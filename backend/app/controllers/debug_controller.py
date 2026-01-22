from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.debug_service import get_users_list, get_all_data, get_all_restaurants

# controlliamo l'inserimento completo di tutto nel db dopo votazione e degli utenti magari
router = APIRouter()


@router.get("/all_users", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = get_users_list(db)
    return users


@router.get("/all_votes", status_code=status.HTTP_200_OK)
def get_all_votes(db: Session = Depends(get_db)):
    restaurants = get_all_restaurants(db)
    datas = get_all_data(db)
    return {"restaurants": restaurants, "datas": datas}