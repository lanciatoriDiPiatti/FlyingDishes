from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.controllers.users_controller import router as users_router

from app.db.session import engine          # <- adatta import
from app.db.base import Base               # <- adatta import
import app.models                          # <- importa tutti i modelli
app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])



