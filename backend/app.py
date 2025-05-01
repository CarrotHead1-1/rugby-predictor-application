from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import matplotlib.pyplot as plt
import pandas as pd
from elo import *

app = FastAPI()

matchResults = pd.read_csv('backend\data\matchResults2018-2025.csv')
matchResults = matchResults[matchResults.columns.drop('rugbypassURL')]

#set up next js access to api 
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://localhost:3000'],
    allow_methods = ["*"],
    allow_headers=["*"],
)


#get global dataset


#get current season schedule 

#get elo 
@app.get('/elo')
def getEloGraph():


    processMatchElo(df = matchResults)
    path = plotEloChange()

    print(path)
#get head to head results


getEloGraph()