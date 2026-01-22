# Here we implement all the logic that involves votations, like creating, updating, deleting votations, counting votes, etc.
from sqlalchemy import null
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.food import Food
from app.models.day import Day
import app.algo as algo
from sqlalchemy.orm.attributes import flag_modified


# Here we implement function to submit votation
def submit_votation(db: Session, voter_id: int, day_votes: list[int], food_votes: list[int]):
    # 1. Controllo utente con HTTPException
    user = db.query(User).filter(User.id == voter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.has_voted:
        raise HTTPException(status_code=400, detail="User has already voted")

    user.has_voted = True

    # 2. Ottimizzazione: Caricamento batch per i giorni
    days = db.query(Day).filter(Day.id.in_([i + 1 for i in range(len(day_votes))])).all()
    day_map = {d.id: d for d in days}
    for index, vote in enumerate(day_votes):
        day = day_map.get(index + 1)
        if day:
            day.votes.append(vote)
            flag_modified(day, "votes") # Necessario se non usi MutableList [web:20]

    # 3. Ottimizzazione: Caricamento batch per i ristoranti
    foods = db.query(Food).filter(Food.id.in_([i + 1 for i in range(len(food_votes))])).all()
    food_map = {f.id: f for f in foods}
    for index, vote in enumerate(food_votes):
        food = food_map.get(index + 1)
        if food:
            food.votes.append(vote)
            flag_modified(food, "votes")

    # 4. Elaborazione e persistenza
    init_avg_computation(db)
    db.commit() # Salva tutte le modifiche in una singola transazione [web:12]
    db.refresh(user)


current_avg_list_days = []
current_mean_list_days = []
current_avg_list_foods = []
current_mean_list_foods = []
# Now we inmplement the function that starts the process of average computation
def init_avg_computation(db: Session):
    
    # for loop that cycles on all the days and foods entitites
    # takes the votes array of each entity
    # and calls the avg_computer function that computes the average
    # finally saves the avg in the current_avg field of each entity
    days = db.query(Day).all()
    for day in days:
        day.current_avg = calculate_average(day.votes)
        current_avg_list_days.append(day.current_avg)

    foods = db.query(Food).all()
    for food in foods:
        food.current_avg = calculate_average(food.votes)
        current_avg_list_foods.append(food.current_avg)


def calculate_average(votes_list: list[int]) -> float:
    if not votes_list:
        return 0.0
    else:
        return algo.calculate_average(votes_list)
    
def calculate_pvariance(votes_list: list[float]) -> float:
    if not votes_list:
        return 0.0
    else:
        return algo.calculate_pvariance(votes_list)
    
def final_choice_days(average: list[int], mean: list[float]) -> int:
    return algo.final_choice(current_avg_list_days, current_mean_list_days)

def final_choice_foods(average: list[int], mean: list[float]) -> int:
    return algo.final_choice(current_avg_list_foods, current_mean_list_foods)

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
