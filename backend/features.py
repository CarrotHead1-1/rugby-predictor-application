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
    #pastMatches = df2[df2["Season"].isin(['18/19', '19/20', '20/21', '21/22', '22/23', '23/24', '24/25'])]
    matches = df2[df2.columns.drop('rugbypassURL')]

    print(processMatchH2H(matches))
    #get elo from past seasons till season with data
    
    eloDf, h2hDf = processPastMatches(matches)
    mergedDf = pd.concat([eloDf, h2hDf], axis=1)
    final = mergedDf.loc[:, ~mergedDf.columns.duplicated()]

    
    print(final.head(100))
    return 



if __name__ == "__main__":
    features()