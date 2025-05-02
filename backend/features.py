import pandas as pd
from elo import *
from h2h import *


def getAllMatchResults():
    try:
        return pd.read_csv('backend\data\matchResults2018-2025.csv')
         
    except FileNotFoundError:
        return None

def getAllMatchData():
    try:
        return pd.read_csv('backend/data/premiershipMatchData22-25.csv')
    
    except FileNotFoundError:
        return None

def processPastMatches(df):

    eloRatings = processMatchElo(df)
    h2h = processMatchH2H(df)

    return eloRatings, h2h

def getResult(row):
    if row["HomeScore"] > row["AwayScore"]:
        return "HomeWin"
    elif row["AwayScore"] > row["HomeScore"]:
        return "AwayWin"
    else:
        return "Draw"
  
def features():

    #get match data dataset
    df1 = getAllMatchData()

    df2 = getAllMatchResults()
    #pastMatches = df2[df2["Season"].isin(['18/19', '19/20', '20/21', '21/22', '22/23', '23/24', '24/25'])]
    matches = df2[df2.columns.drop('rugbypassURL')]
    #print(matches)
    #get elo from past seasons till season with data
    
    eloDf, h2hDf = processPastMatches(matches)
    #merges the eloDf, h2hDf, and matchResultsDf
    mergedDf = pd.concat([matches, eloDf, h2hDf], axis=1)
    final = mergedDf.loc[:, ~mergedDf.columns.duplicated()]

    #filter out seasons not in the matchDataDf
    filtered = final[final['Season'].isin(['22/23', '23/24', '24/25'])]
    filtered = filtered.reset_index(drop=True)
    #print(filtered)

    featuresDf = df1.merge(
        filtered, 
        on = ["HomeTeam", "AwayTeam", "Season", "Round", "HomeScore", "AwayScore"],
        how='right')
    
    featuresDf["Result"] = featuresDf.apply(getResult, axis = 1)
    #print(featuresDf.head(10))
    


    return featuresDf



if __name__ == "__main__":
    features()