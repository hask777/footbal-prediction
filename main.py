from fastapi import FastAPI, Depends
from db import models
from db.database import engine
from typing import Optional
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status

from routers import predictions
from routers import events
from routers import api
from routers import finished
from routers import scheduled
from routers import league
from routers import country
# from routers import performance
# from routers import fixtures



app = FastAPI()
app.include_router(predictions.router)
app.include_router(events.router)
app.include_router(scheduled.router)
app.include_router(finished.router)
app.include_router(api.router)
app.include_router(league.router)
app.include_router(country.router)
# app.include_router(performance.router)
# app.include_router(fixtures.router)


models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/logos", StaticFiles(directory="img-scraper"), name="logos")

@app.get('/')
async def root():
    
     return RedirectResponse("http://127.0.0.1:8000/events")
    