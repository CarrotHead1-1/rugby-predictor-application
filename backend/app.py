
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os 
import matplotlib.pyplot as plt
import pandas as pd
import pickle 
from features import features
from h2h import *
from elo import *
from modelTest import *

app = FastAPI()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data", "matchResults2018-2025.csv")
STATIC_PATH = os.path.join(BASE_PATH, "static")
df = pd.read_csv(DATA_PATH)
df = df[df.columns.drop('rugbypassURL')]

df2 = pd.read_csv(os.path.join(BASE_PATH, "data", "premiershipMatchData22-25.csv"))
#mount static files 
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#get global dataset

#get rf model
with open("static/rf_model.pkl", "rb") as f:
    model = pickle.load(f)

#get current season schedule
@app.get('/seasons')
def getSeasons():
    filtered = df['Season'].unique()
    seasons = filtered.tolist()
    return JSONResponse(content = {'seasons' : seasons})

@app.get('/matches')
def getMatches(season):
    filtered = df[df['Season'].isin([season])]
    matches = filtered.to_dict(orient="records")
    return JSONResponse(content = {'matches' : matches})

#get elo 
@app.get('/elo')
def getEloGraph():
    processMatchElo(df)
   
    history = getHistroy()
    

    elos = {}
    for team, ratings in history.items():
        peak = max(ratings)
        current = ratings[-1]
        elos[team] = {"Peak Elo" : peak, "Current Elo": current}

    image_path = plotEloChange()
    
    response = {
        "image_path" : image_path,
        "elos" : elos
    }

    return JSONResponse(content = response)
    #return FileResponse(image_path, media_type="image/png")

def dataSetup(df):
    df = encodeValues(df)
    df = removeMissing(df)

    X, y = selectFeatures(df)
    return X, y

@app.get("/predictions")
def getPredictions(home, away, season, round):
    matchData = features(df, df2)
    #print(matchData)
    #find the coresponding game => home, away, season, round
    fixture = matchData.loc[
        (matchData["HomeTeam"] == home) 
        & (matchData["AwayTeam"] == away) 
        & (matchData["Season"] == season)
        & (matchData["Round"] == round)]
    print(fixture)
    match_X, _ = dataSetup(fixture)
    print(match_X)
    pred = model.predict(match_X)
    return JSONResponse(content = {"prediction" : pred.tolist()})
    #data = matchData.to_dict(orient="records")
    #return JSONResponse(content = {'data' : data})

#get head to head results
@app.get('/h2h')
def getH2H():
    processMatchH2H(df)
    h2h = h2hResults()
    #print(h2h)
    return JSONResponse(content = {'h2h' : h2h})