import os
import sys

backend_data_path = os.path.join(os.path.dirname(__file__), '../backend/data')
sys.path.append(backend_data_path)
print('sys.path after append:', sys.path)
print('Modules in backend/data:', os.listdir(backend_data_path))


from get_all_leagues import sqlite_get_all_leagues, sqlite_insert_leagues #type:ignore

import uvicorn 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

class League(BaseModel):
    league_id: int
    league_name: str
    country_name: str
    country_code: Optional[str]
    league_type: str
    league_logo: str

class LeagueSeasons(BaseModel):
    league_id: int
    season: str


app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# server-rendered templates
templates = Jinja2Templates(directory="football-and-spark/frontend/templates")

origins = [
    "http://localhost:3000"]


#CORS: CROSS ORIGIN RESOURCE SHARING
# -- ability to grant access to resources from different origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # allow all methods (GET, POST, etc.)
    allow_headers=["*"], # allow all headers
)

@app.get("/leagues", response_model=List[League])
async def get_leagues():
    # query from sqlite db
    leagues = sqlite_get_all_leagues()
    return leagues

@app.post("/leagues", response_model=League)
async def create_leagues(leagues: List[League]):
    # Insert leagues into the database
    sqlite_insert_leagues(leagues)
    return leagues


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

