import requests
import json

import sys
sys.path.append("..")
# fastapi
from fastapi import Depends, APIRouter, Request, Form
# db
from db import models
from db.database import engine
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal, Base

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from datetime import date
import time

today = str(date.today())

def store(today):

    

    url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{today}"

    payload = ""
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


    response = requests.request("GET", url, data=payload, headers=headers).json()

    # print(response)

    with open('json/all.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=4, ensure_ascii=False)


    db = SessionLocal() 

    db.query(models.Event).delete()
    db.commit()
  

    for event in response['events']:

        with Session(engine) as session:

                new_event = models.Event()

                date = str(datetime.fromtimestamp(event['startTimestamp']))
                # print(date)

                date = date.split(' ')
                dates = date[0]
                time = date[1][:-3]
              

                try:          
                    # tournament
                    new_event.tournament_name = event['tournament']['name']
                    new_event.tournament_slug = event['tournament']['slug']
                    new_event.tournament_category = event['tournament']['category']['name']
                    new_event.tournament_id = event['tournament']['category']['id']
                    new_event.tournament_flag = event['tournament']['category']['flag']
                    new_event.tournament_unique_id = event['tournament']['uniqueTournament']['id']
                    new_event.tournament_players_stat = event['tournament']['uniqueTournament']['hasEventPlayerStatistics']
                    # round
                    # new_event.round = event['roundInfo']['round']
                    # new_event.round_name = event['roundInfo']['name']
                    # winner
                    new_event.winner_code = event['winnerCode']
                    # home_team
                    new_event.home_team_name = event['homeTeam']['name']
                    new_event.home_team_shortname = event['homeTeam']['shortName']
                    new_event.home_team_code = event['homeTeam']['nameCode']
                    new_event.home_team_type = event['homeTeam']['type']
                    new_event.home_team_id = event['homeTeam']['id']
                    new_event.home_team_country_alpha2 = event['homeTeam']['country']['alpha2']
                    new_event.home_team_country_name = event['homeTeam']['country']['name']
                    new_event.home_team_primary_color = event['homeTeam']['teamColors']['primary']
                    new_event.home_team_secondary = event['homeTeam']['teamColors']['secondary']
                    new_event.home_team_text = event['homeTeam']['teamColors']['text']
                    # # home_team
                    new_event.away_team_name = event['awayTeam']['name']
                    new_event.away_team_shortname = event['awayTeam']['shortName']
                    new_event.away_team_code = event['awayTeam']['nameCode']
                    new_event.away_team_type = event['awayTeam']['type']
                    new_event.away_team_id = event['awayTeam']['id']
                    new_event.away_team_country_alpha2 = event['awayTeam']['country']['alpha2']
                    new_event.away_team_country_name = event['awayTeam']['country']['name']
                    new_event.away_team_primary_color = event['awayTeam']['teamColors']['primary']
                    new_event.away_team_secondary = event['awayTeam']['teamColors']['secondary']
                    new_event.away_team_text = event['awayTeam']['teamColors']['text']
                    # # stats
                    new_event.home_score = event['homeScore']
                    new_event.away_score = event['awayScore']
                    new_event.time = event['time']
                    new_event.changes = event['changes']
                    # event
                    new_event.has_global_highlights = event['hasGlobalHighlights']
                    # new_event.has_event_players_stat = event['hasEventPlayerStatistics']
                    # new_event.has_event_players_heat_map = event['hasEventPlayerHeatMap']
                    # new_event.detailID = event['detailId']
                    new_event.event_id = event['id']
                    new_event.status = event['status']['type']
                    new_event.start_timestamp = event['startTimestamp']
                    new_event.date = dates
                    new_event.time = time
                    new_event.slug = event['slug']
                    new_event.final_result_only = event['finalResultOnly']

                    session.add_all([new_event])
                    session.commit()
                except:
                     continue
                
    print('DO!!!')
                


while True:
    store(today)
    time.sleep(60)
