# Here we implement all the logic that involves votations, like creating, updating, deleting votations, counting votes, etc.
from sqlalchemy import null
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.food import Food
from app.models.day import Day
import app.algo

# Here we implement function to submit votation
def submit_votation(db: Session, voter_id: int, day_votes: list[int], food_votes: list[int]):
    # firstly we need to check if the User that is trying to vote has already voted
    # This logic is not implemented yet, but we will assume that the voter_id is valid

    user= db.query(User).filter(User.id == voter_id).first()
    if not user:
        raise Exception("User not found")
    if user.has_voted:
        raise Exception("User has already voted")
    
    # If the user has not voted yet, we set his has_voted field to True
    user.has_voted = True
    

    # We take the array of day_votes and add all the elements to the corresponding day entity
    # to get the right day, we look at the index of the array
    for index, vote in enumerate(day_votes):
        day = db.query(Day).filter(Day.id == index + 1).first()
        if day:
            day.votes.append(vote)
    
    # We do the same thing for the Ristoranti (food)
    for index, vote in enumerate(food_votes):
        food = db.query(Food).filter(Food.id == index + 1).first()
        if food:
            food.votes.append(vote)
    
    # After updating the votes arrays, we need to recalculate the averages
    init_avg_computation(db)

    # Final commit of the db after modifications
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


def calculate_average(votes_list: list[int]) -> float:
    if not votes_list:
        return 0.0
    return sum(votes_list) / len(votes_list)

def get_current_avgs(db : Session):
    # preparo un array per salvare le medie dei ristoranti
    foods = db.query(Food).all()
    food_avgs = []
    for food in foods:
        food_avgs.append(food.current_avg)

    # preparo un array per media delle date
    data_avgs = []
    dates = db.query(Day).all()
    for date in dates:
        data_avgs.append(date.current_avg)

    return {"food": food_avgs, "days":data_avgs}
