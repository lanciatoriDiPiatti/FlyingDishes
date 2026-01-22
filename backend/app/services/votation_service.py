# Here we implement all the logic that involves votations, like creating, updating, deleting votations, counting votes, etc.
from sqlalchemy import null
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.food import Food
from app.models.day import Day
import app.algo as algo
from sqlalchemy.orm.attributes import flag_modified
from fastapi import HTTPException, status


# Here we implement function to submit votation
def submit_votation(db: Session, voter_id: int, day_votes: list[int], food_votes: list[int]):
    # cerchiamo l'utente nel db
    user = db.query(User).filter(User.id == voter_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) Controllo has_voted
    if user.has_voted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already voted")

    user.has_voted = True
    
    # Se non ha ancora votato set della flag su true
    user.has_voted = True

    # Prendo i dati della votazione dei giorni uno alla vola seguendo l'indice
    for index in range(len(day_votes)):
        # ogni indice = id del giorno nella tabella del db
        # trovo il giorno corrispondente
        day = db.query(Day).filter(Day.id == index + 1).first()
        # aggiungo il voto all'entità
        day.votes.append(day_votes(index))
        flag_modified(day, "votes")

    # Faccio lo stesso per i ristoranti
    for index in range(len(food_votes)):
        food = db.query(Food).filter(Food.id == index + 1).first()
        # aggiungo il voto all'entità
        food.votes.append(food_votes(index))
        flag_modified(food, "votes")

    # Una volta inseriti tutti i dati, chiamo il calcolo della media
    init_avg_computation(db)

    # commit del db
    db.commit()



# Now we inmplement the function that starts the process of average computation
def init_avg_computation(db: Session):
    
    # for loop that cycles on all the days and foods entitites
    # takes the votes array of each entity
    # and calls the avg_computer function that computes the average
    # finally saves the avg in the current_avg field of each entity
    days = db.query(Day).all()
    for day in days:
        day.current_avg = calculate_average(day.votes)

    foods = db.query(Food).all()
    for food in foods:
        food.current_avg = calculate_average(food.votes)


def calculate_average(votes_list: list[int], id) -> float:
    if not votes_list:
        return 0.0
    else:
        return algo.calculate_average(votes_list)
    

def calculate_pvariance(votes_list: list[float]) -> float:
    if not votes_list:
        return 0.0
    else:
        return algo.calculate_pvariance(votes_list)
    

# Ritorna l'indice corrispondente all'entità con la votazione più alta
def final_choice_days(db: Session):
    # Prende la lista delle medie:
    day_avg_list = []
    # Preparo lista delle varianze:
    day_var_list = []
    # La riempie con tutti i dati presi da tutte le entità Day
    days = db.query(Day).all()
    for day in days:
        day_avg_list.append(day.current_avg)
        day_var_list.append(day.current_var)

    # Per ultima cosa chiamiamo l'algoritmo di scelta
    return algo.final_choice(day_avg_list, day_var_list)



def final_choice_foods(db: Session):
    # Prende la lista delle medie:
    food_avg_list = []
    # Preparo lista delle varianze:
    food_var_list = []
    # La riempie con tutti i dati presi da tutte le entità Day
    foods = db.query(Food).all()
    for food in foods:
        food_avg_list.append(food.current_avg)
        food_var_list.append(food.current_var)

    # Per ultima cosa chiamiamo l'algoritmo di scelta
    return algo.final_choice(food_avg_list, food_var_list)


def get_current_avgs(db: Session):
    # Inizializza con liste vuote [], non con null
    food_avgs = []
    foods = db.query(Food).all()
    for food in foods:
        food_avgs.append(food.current_avg)

    data_avgs = []
    dates = db.query(Day).all()
    for date in dates:
        # Usa 'date' (l'istanza del ciclo), non 'Day' (la classe)
        data_avgs.append(date.current_avg)

    return {"food": food_avgs, "days": data_avgs} 
