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
import time

# define router
router = APIRouter(
    prefix='/api',
    tags=['api'],
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
@router.get('/',)
async def get_all(request: Request, db: Session = Depends(get_db)):
    games = db.query(models.Event).all()
    # print(games)

    return {"games": games}



# # router all
@router.get('/tournamnets',)
async def get_all(request: Request, db: Session = Depends(get_db)):
    url = 'https://api.sofascore.com/api/v1/config/unique-tournaments/BY'

    headers = {
        "authority": "api.sofascore.com",
        "accept": "*/*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl-PL;q=0.6,pl;q=0.5",
        "cache-control": "max-age=0",
        "if-none-match": "W/^\^2c2d5bd32d^^",
        "origin": "https://www.sofascore.com",
        "referer": "https://www.sofascore.com/",
        "sec-ch-ua": "^\^Not.A/Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^114^^, ^\^Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers).json()
    print(response)

    return response


