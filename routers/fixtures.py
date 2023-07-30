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

from datetime import date


# define router
router = APIRouter(
    prefix='/fixtures',
    tags=['fixtures'],
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


# router all
@router.get('', response_class=HTMLResponse)
async def get_all(request: Request, db: Session = Depends(get_db)):
    today = str(date.today())

    leagues = db.query(models.Event2).distinct(models.Event2.league_name)
    
    games = db.query(models.Event2).all()
    
    tournaments = db.query(models.Event2).distinct(models.Event2.league_name)

    countries = db.query(models.Event2).distinct(models.Event2.league_country)


    return templates.TemplateResponse("all2.html", {
        "request": request,
        "games": games,
        "tournaments": tournaments,
        "leagues": leagues,
        "countries": countries,
    })

# router all
@router.get('/event/{event_id}', response_class=HTMLResponse)
async def get_all(request: Request, event_id: int, db: Session = Depends(get_db)):

    game = db.query(models.Event2).filter(models.Event2.event_id == event_id).first()
  
    return templates.TemplateResponse("game.html", {
        "request": request,
        "game": game
    })