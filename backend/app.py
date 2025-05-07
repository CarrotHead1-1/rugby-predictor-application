
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

featureDf,eloDf, h2hDf = features(df, df2)


def mergeElo():
    mergedDf = pd.concat([df, eloDf], axis=1)
    mergedElo = mergedDf.loc[:, ~mergedDf.columns.duplicated()]
    return(mergedElo)

mergedElo = mergeElo()


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

with open("static/rf_accuracyReport.json") as f:
    report = json.load(f)

try:
    with open ('/static/model_predictions.json') as f:
        modelPredictions = json.load(f)
except:
    modelPredictions = {}

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
def getElo(home, away, season, round):

    match = mergedElo.loc[
        (mergedElo["HomeTeam"] == home) 
        & (mergedElo["AwayTeam"] == away) 
        & (mergedElo["Season"] == season)
        & (mergedElo["Round"] == round)]

    return JSONResponse(content={
        "homeElo" : int(match["HomeElo"].values),
        "awayElo" : int(match["AwayElo"].values),
        "eloDiff" : int(match["EloDiff"].values)
    })

@app.get('/eloGraph')
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

def dataSetup(df):
    df = encodeValues(df)
    df = removeMissing(df)

    X, y = selectFeatures(df)
    return X, y

def getFeatures(df1, df2):
    return features(df1, df2)

@app.get("/predictions")
def getPredictions(home, away, season, round):
    #check for season 
    if (season == '18/19' or 
        season =='19/20' or 
        season == '20/21' or 
        season == '21/22'):
        return None
    
    #create key 
    key = f"{home}-{away}-{season}-{round}"
    if modelPredictions:
        if key in modelPredictions:
            return JSONResponse(content={"prediction" : modelPredictions[key]})
    
    matchData, _, _ = getFeatures(df, df2)

    fixture = matchData.loc[
        (matchData["HomeTeam"] == home) 
        & (matchData["AwayTeam"] == away) 
        & (matchData["Season"] == season)
        & (matchData["Round"] == round)]

    match_X, _ = dataSetup(fixture)
    pred = model.predict(match_X)
    prediction = int(pred[0])

    if prediction == 0:
        predictionText = "AwayWin"
    elif prediction == 2:
        predictionText = "HomeWin"
    else:
        predictionText = "Draw"

    #add new prediction to storedPredictions
    modelPredictions[key] = [home, away, season, round, predictionText]

    #store new predictions
    with open("static/model_predictions.json", "w") as f:
        json.dump(modelPredictions, f, indent=4)

    return JSONResponse(content={"prediction" : modelPredictions[key]})

@app.get('/modelCount')
def getModelCount():

    #set up counters
    correct = 0
    incorrect = 0

    for key, prediction in modelPredictions.items():
        home,away,season,round_, predictedResult = prediction

        #search for fixture
        actual = featureDf.loc[
            (featureDf["HomeTeam"] == home) &
            (featureDf["AwayTeam"] == away) &
            (featureDf["Season"] == season) &
            (featureDf["Round"] == round_),
            "Result"
        ]

        #create comparison key
        comparison = f"{home}-{away}-{season}-{round_}"
        if key == comparison:
            if predictedResult == actual.iloc[0]:
                correct += 1
            else:
                incorrect += 1 
        
    total = correct + incorrect

    return JSONResponse(content={
        "correctPredictions" : correct,
        "incorrectPredictions" : incorrect,
        "totalPredictions" : total,
        "Accuracy" : round((correct / total) * 100, 2) if total > 0 else 0.0 
    })

@app.get("/modelReport")
def getModelReprt():
    return report

#get head to head results
@app.get('/h2h')
def getH2H():
    processMatchH2H(df)
    h2h = h2hResults()
    #print(h2h)
    return JSONResponse(content = {'h2h' : h2h})