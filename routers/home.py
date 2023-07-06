import sys
sys.path.append("..")
# fastapi
from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
# db
from db import models
from sqlalchemy import distinct, select, table, inspect

from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
# html
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import requests

# define router
router = APIRouter(
    prefix='/home',
    tags=['home'],
    responses={404: {"description": "Not found"}}
)

# database init
models.Base.metadata.create_all(bind=engine)

# enable templates
templates = Jinja2Templates(directory="templates")

# database connection
def get_db():
    try:  
        db = SessionLocal()  
        yield db
    finally:
        db.close()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

# router all
@router.get('', response_class=HTMLResponse)
async def get_all(request: Request, db: Session = Depends(get_db)):
    games = db.query(models.Event).all()
    # print(games)
    
    tournamets = db.query(models.Event).distinct(models.Event.tournament_name)

    for tournament in tournamets:
        print(object_as_dict(tournament))

    return templates.TemplateResponse("home.html", {"request": request, "games": games, "tournamets": tournamets})

