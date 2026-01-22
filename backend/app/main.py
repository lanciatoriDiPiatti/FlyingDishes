from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.auth_controller import router as auth_router
from app.controllers.users_controller import router as users_router
from app.controllers.votation_controller import router as votation_router
from app.controllers.debug_controller import router as debug_router

from app.db.session import engine          # <- adatta import
from app.db.base import Base               # <- adatta import
import app.models                          # <- importa tutti i modelli
app = FastAPI()

# Definisci le origini consentite per CORS
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
]

# Aggiungi il middleware CORS all'applicazione
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(votation_router, prefix= "/votation", tags=["votation"])
app.include_router(debug_router, prefix = "/debug", tags = ["debug"])



