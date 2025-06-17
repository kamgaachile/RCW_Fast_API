import sys, os
# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI, Request,Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from  fastapi.templating import Jinja2Templates
import  uvicorn
from dash_app import app as dash_app
import requests


#crer lobjet FastAPI
app = FastAPI()

# obtenir un chemin absolu vers le dossier parent
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))

# obtenir un chemin absolu vers le dossier parent
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

#configurer le  modele jinja2 pour le rendu des fichier html
templates = Jinja2Templates(directory=parent_dir)

# servir des fichiers statiques
app.mount("/static", StaticFiles(directory=static_dir))

# montrer l'application Dash sous le chemin /dashboard
app.mount("/dashboard", WSGIMiddleware(app=dash_app.server))


users = {"admin": "123"}

EXTERNAL_URL_API="http://127.0.0.1:8000/info"

def get_external_api_data():
    try:
        response= requests.get(EXTERNAL_URL_API)
        return response.json()
    except Exception as e :
        return{
            "date": "N/A",
            "time": "N/A",
            "weather": {
                "temperature": "N/A",
                "description": "N/A",
                "wind_speed": "N/A",
                "humidity": "N/A"
            
            }
        }

@app.get("/")
async def home_page(request: Request):
    info = get_external_api_data()
    return templates.TemplateResponse('home.html', {'request': request, 'info': info})

# recupere et affiche le formulaire  login.html
@app.get("/login")
async def login_page(request: Request):  # ⚠️ renommé ici
    return templates.TemplateResponse('login.html', {'request': request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="authorisation", value="bearer token", httponly=True)
        return response
    return templates.TemplateResponse('login.html', {'request': request, 'error': 'Invalid username or password'})


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="authoriastion")
    return response
