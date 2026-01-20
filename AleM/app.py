import os
from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database import conn, create_table
from methods import DbUser
from config import load_config

# --- App and Lifespan Management ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    print("Application startup...")
    print("Creating database tables if they don't exist...")
    create_table()
    yield
    print("Application shutdown...")
    print("Closing database connection...")
    conn.close()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# --- Definizione delle Route ---

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/PostUser")
def postUser(request: Request, username: str = Form(None), password: str = Form(None)):
    db = DbUser()
    db.create_user(username=username, password=password)
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/getUser")
def getUser(request: Request, username: str):
    db = DbUser()
    try:
        db.get_user(username)
        return templates.TemplateResponse("home.html", {"request": request})
    except Exception as e:
        print(f"Errore durante il recupero dell'utente: {e}")
    
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/register")
def register(request: Request, registration_name: str = Form(None), registration_pswd: str = Form(None)):
    #SE NON C'È NE IL NOME UTENTE NE LA PASSWORD PER REGISTRARSI
    if not registration_name or not registration_pswd:
        context = {"request": request, "error": "Nome utente e password sono obbligatori."}
        return templates.TemplateResponse("home.html", context, status_code=status.HTTP_400_BAD_REQUEST)

    #ESEGUE LA REGISTRAZIONE
    if DbUser.create_user(username=registration_name, password=registration_pswd):
        return RedirectResponse(url="/submit", status_code=status.HTTP_303_SEE_OTHER)
    else:
        #ESISTE GIÀ L'UTENTE
        context = {"request": request, "error": "L'utente esiste già. Scegli un altro nome utente."}
        return templates.TemplateResponse("home.html", context, status_code=status.HTTP_409_CONFLICT)


@app.post("/login")
def login(request: Request, login_name: str = Form(None), login_pswd: str = Form(None)):
    # SE NON C'È NE LA PASSWORD NE IL NOME UTENTE
    if not login_name or not login_pswd:
        context = {"request": request, "error": "Nome utente e password sono obbligatori."}
        return templates.TemplateResponse("home.html", context, status_code=status.HTTP_400_BAD_REQUEST)
    
    #ESEGUE IL LOGIN
    if DbUser.check_auth(username=login_name, password=login_pswd):
        return RedirectResponse(url="/submit", status_code=status.HTTP_303_SEE_OTHER)
    
    #NON AUTORIZZATO
    else:
        context = {"request": request, "error": "L'utente esiste già. Scegli un altro nome utente."}
        return templates.TemplateResponse("home.html", context, status_code=status.HTTP_401_UNAUTHORIZED)
    
if __name__ == "__main__":
    config = load_config()
    create_table()
    