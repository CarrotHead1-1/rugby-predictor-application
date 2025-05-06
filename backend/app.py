
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

featureDf = features(df, df2)

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
    match = featureDf.loc[
        (featureDf["HomeTeam"] == home) 
        & (featureDf["AwayTeam"] == away) 
        & (featureDf["Season"] == season)
        & (featureDf["Round"] == round)
    ]

    
    return JSONResponse(content={
        "homeElo" : int(match["HomeElo"].values[0]),
        "awayElo" : int(match["AwayElo"].values[0]),
        "eloDiff" : int(match["EloDiff"].values[0])
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
    #return FileResponse(image_path, media_type="image/png")

def dataSetup(df):
    df = encodeValues(df)
    df = removeMissing(df)

    X, y = selectFeatures(df)
    return X, y

def getFeatures(df1, df2):
    return features(df1, df2)

@app.get("/predictions")
def getPredictions(home, away, season, round):

    #check if the prediction exsists
    predictionFile = os.path.join(STATIC_PATH, "predictions.json")

    if os.path.exists(predictionFile):
        with open(predictionFile, "r") as f:
            predictions = json.load(f) 
    else:
        predictions = []

    #check for prediction
    for entry in predictions: 
        if (entry["HomeTeam"] == home and entry["AwayTeam"] == away and entry["Season"] == season and entry["Round"] == round):
            return JSONResponse(content={"prediction": entry["predictionText"]})
    
    #generate prediction
    matchData = getFeatures(df, df2)
    
    #print(matchData)
    #find the coresponding game => home, away, season, round
    fixture = matchData.loc[
        (matchData["HomeTeam"] == home) 
        & (matchData["AwayTeam"] == away) 
        & (matchData["Season"] == season)
        & (matchData["Round"] == round)]
    
    if fixture.empty:
        return JSONResponse(content={"error" : "Match not found"})
    
    match_X, _ = dataSetup(fixture)
    pred = model.predict(match_X)
    prediction = int(pred[0])

    if prediction == 0:
        predictionText = "AwayWin"
    elif prediction == 2:
        predictionText = "HomeWin"
    else:
        predictionText = "Draw"

    #add new prediction 
    newPrediction = {
        "HomeTeam" : home,
        "AwayTeam" : away,
        "Season" : season,
        "Round" : round,
        "prediciton" : prediction,
        "predictionText" : predictionText
    }

    predictions.append(newPrediction)
    with open(predictionFile, "w") as f:
        json.dump(predictions, f, indent=4)

        return JSONResponse(content = {"Prediction" : predictionText})

    
    #data = matchData.to_dict(orient="records")
    #return JSONResponse(content = {'data' : data})

@app.get('/modelCount')
def getModelCount():

    predictionsFile = os.path.join(STATIC_PATH, "predictions.json")
    
    if not os.path.exists(predictionsFile):
        return JSONResponse(content={"error" : "No predicitons found"})
    
    with open (predictionsFile, "r") as f:
        predictions = json.load(f)

    matchData = getFeatures(df, df2)
    
    correct = 0
    incorrect = 0 

    for entry in predictions:
        home = entry["HomeTeam"]
        away = entry["AwayTeam"]
        season = entry["Season"]
        round = entry["Round"]
        predicted = entry["predictionText"]

        fixture = matchData.loc[
            (matchData["HomeTeam"] == home) 
            & (matchData["AwayTeam"] == away) 
            & (matchData["Season"] == season)
            & (matchData["Round"] == round)]
        
        
        
        actual = fixture["Result"].values
        print(predicted, actual)
        if predicted == actual:
            correct += 1
        else:
            incorrect += 1
    
    return JSONResponse(content = {
        "CorrectPredictions" : correct,
        "IncorrectPredictions" : incorrect,
        "TotalPredictions" : correct + incorrect,
        "Accuracy" : float(correct / (correct + incorrect)) * 100
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