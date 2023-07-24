import requests
import json
from db.database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import models
from datetime import date, datetime
from datetime import datetime, date
import time


today = str(date.today())

print(today)

url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"

querystring = {f"market":"classic","iso_date":{today}}
# querystring = {f"market":"classic","iso_date":"2023-07-23"}

headers = {
	"X-RapidAPI-Key": "b606334c27msh64b0f8f28715854p184c23jsn1a16e1bb37ec",
	"X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
}

events = requests.get(url, headers=headers, params=querystring).json()

with open('json/predictions.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, indent=4, ensure_ascii=False)

db = SessionLocal() 

# db.query(models.Prediction).delete()
# db.commit()
  
for event in events["data"]:
        
	dates = event['start_date'].split('T')
	dated = dates[0]
	time = dates[1][:-3]
        
	print(dates)

	game = models.Prediction()

	game.home_team = event['home_team']
	game.away_team = event['away_team']
	game.event_id = event['id']
	game.market = event['market']
	game.competition_name = event['competition_name']
	game.prediction = event['prediction']
	game.competition_cluster = event['competition_cluster']
	game.status = event['status']
	game.federation = event['federation']
	game.is_expired = event['is_expired']
	game.season = event['season']
	game.result = event['result']
	game.start_date = event['start_date']
	game.date = dated
	game.time = time
	game.last_update_at = event['last_update_at']
	game.odds = event['odds']
        
	db.add(game)
	db.commit()