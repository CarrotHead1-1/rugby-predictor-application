import pandas as pd
from elo import *
from h2h import *


def getAllMatchResults():
    try:
        return pd.read_csv('backend\datasets\matchResults2018-2025.csv')
         
    except FileNotFoundError:
        return None

def getAllMatchData():
    try:
        return pd.read_csv('backend\datasets\premiershipMatchData22-25.csv')
    
    except FileNotFoundError:
        return None

def processPastMatches(df):

    eloRatings = processMatchElo(df)
    h2h = processMatchH2H(df)

    return eloRatings, h2h

def features():

    #get match data dataset
    df1 = getAllMatchData()

    df2 = getAllMatchResults()
    pastMatches = df2[df2["Season"].isin(['18/19', '19/20', '20/21', '21/22'])]
    pastMatches = pastMatches[pastMatches.columns.drop('rugbypassURL')]
    #get elo from past seasons till season with data
    
    eloRatings, h2h = processPastMatches(pastMatches)
    print(eloRatings)
    print(h2h)
    return 



if __name__ == "__main__":
    features()