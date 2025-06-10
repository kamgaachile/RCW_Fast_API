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

@app.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

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
