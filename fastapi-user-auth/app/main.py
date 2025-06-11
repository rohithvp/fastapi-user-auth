from fastapi import FastAPI ,Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from sqlalchemy.orm import Session

from app import models
from app.database import sessionlocal, engine
from app.models import User
from app.auth_pass import hash_password, verify_password

models.Base.metadata.create_all(bind= engine)


app = FastAPI()
templates= Jinja2Templates(directory="app/templates")   

def get_db():
     db = sessionlocal()
     try:
         yield db
     finally:
         db.close()

@app.get("/register",response_class= HTMLResponse)
def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request  })

@app.post("/register", response_class=HTMLResponse)
def post_register(
     request : Request,
         username: str = Form(...),
         email: str = Form(...),
         password: str = Form(...),
         db: Session = Depends(get_db)
 ):
     user_exists = db.query(User).filter(User.username== username).first()
     if user_exists:
         return templates.TemplateResponse("register.html", {"request": request, "message": "Username is already exists"})
    
     hashed_pw= hash_password(password)
     new_user = User(username = username, email= email, password=hashed_pw)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return RedirectResponse("/", status_code=303)
    


@app.get("/", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def post_login(
     request:Request,    
     username: str = Form(...),
     password: str = Form(...),
     db: Session = Depends(get_db)
 ):
     user = db.query(User).filter(User.username == username).first()
     if not user or not verify_password(password, user.password):
         return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials!"})
    
     return templates.TemplateResponse("dashboard.html", {"request": request, "username": user.username})
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})