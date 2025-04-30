import pandas as pd
import time
from scraper import scrapeData

def getAllMatchResults():
    try:
        return pd.read_csv('matchResults2018-2025.csv')
         
    except FileNotFoundError:
        return None

def getUrls():
    try:
        df =  pd.read_csv('matchResults2018-2025.csv')
        return df['rugbypassURL'].dropna().reset_index(drop=True)
    
    except:
        return 
    
def getSeason(df, season):
    return df[df['Season'].isin([season])]

def getSeasons(df):
    return df[df['Season'].isin(['22/23', '23/24', '24/25'])]

def getRound(df, round):
    return df[df['Round'].isin([round])] 

def convertDtypes(df):
    newDf = df.convert_dtypes()
    return newDf

def createLatestDf(data):
    df = pd.DataFrame([data], columns = ['Home 22m Entries', 'Away 22m Entries', 'Home 22m Conversions', 
        'Away 22m Conversions', 'Home Line Breaks',' Away Line Breaks', 'Home Carries', 'Away Carries', 'Home Kicks',' Away Kicks',
        'Home Post Contact Metres', 'Away Post Contact Metres', 'Home Dominate Tackles', 'Away Dominate Tackles', 'Home Tackles Made',
        'Away Tackles Made','Home Tackles Missed', 'Away Tackles Missed', 'Home Turnovers Won', 'Away Turnovers Won','Home Tackle Turnovers', 'Away Tackle Turnovers', 
        'Home Offloads Allowed', 'Away Offloads Allowed', 'Home 0-3s Ruck Speed','Away 0-3s Ruck Speed', 'Home 3-6s Ruck Speed', 'Away 3-6s Ruck Speed', 
        'Home 6s+ Ruck Speed', 'Away 6s+ Ruck Speed','Home Rucks Won', 'Away Rucks Won'])

    #print("latest df created")
    return df

def createStatsDf(data):
    df = pd.DataFrame([data], columns = ['Home Penalty Goals','Away Penalty Goals', 'Home Tries', 'Away Tries',
        'Home Conversions', 'Away Conversions', 'Home Drop Goals', 'Away Drop Goals','Home Carries', 'Away Carries', 'Home Line Breaks',
        'Away Line Breaks', 'Home Turnovers Lost', 'Away Turnovers Lost', 'Home Turnovers Won', 'Away Turnovers Won', 'Territory Home Try-Line - 22m', 
        'Territory Home 22m - 50m', 'Territory Away 22m - 50m', 'Territory Away Try-Line - 22m', 'Home Territory', 'Away Territory', 
        'Home Possessions Try Line - 22m', 'Home Possession 22m - 50m', 'Home Possession opp 50m - 22m','Home Possession opp 22m - Try Line',
        'Away Possessions Try Line - 22m', 'Away Possession 22m - 50m', 'Away Possession opp 50m - 22m', 'Away Possession opp 22m - Try Line',
        'Home Possession Last 10', 'Away Possession Last 10', 'Home Possession', 'Away Possession', 'Home Scrums', 'Away Scrums', 
        'Home Scrum Wins', 'Away Scrum Wins', 'Home Lineouts', 'Away Lineouts', 'Home Lineout Wins %', 'Away Lineout Wins %', 'Home Restarts Received', 
        'Away Restarts Received', 'Home Restarts Received Win %', 'Away Restarts Received Win %', 'Home Passes', 'Away Passes', 'Home Carries',
        'Away Carries','Home Line Breaks', 'Away Line Breaks', 'Home Turnovers Won',
        'Away Turnovers Won', 'Home Turnovers Lost', 'Away Turnovers Lost', 'Home Penalties Conceded', 'Away Penalties Conceded','Home Yellow Cards',
        'Away Yellow Cards', 'Home Red Cards', 'Away Red Cards', 'Home Tackles Made', 'Away Tackles Made', 'Home Tackles Missed',
        'Away Tackles Missed', 'Home Tackle Completion', 'Away Tackle Completion', 'Home Kicks', 'Away Kicks'])
    
    #print("stats df created")
    return df

def mergeDf(frames):
    df = pd.concat(frames, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    
    return df 

def main():

    # df = getAllMatchResults()
    # testFixture = getSeason(df, '23/24').reset_index(drop=True)
    # #print(testFixture.columns)
    # testMatch = testFixture[testFixture.columns.drop('rugbypassURL')]
    # testMatch = testMatch.loc[0].to_frame().T
    # print(testMatch.shape)
    # latest = createLatestDf([9,12,3.78,1.92,8,6,88,122,24,29,206,277,14,2,139,84,28,20,5,5,2,1,10,10,0.39,0.42,0.3,0.3,0.24,0.23,50,87])
    
    # frames = [testMatch, latest]
    # merged = mergeDf(frames)
    # print(merged)
    #unindet to scrape -- > fixing the merging of data
    
    df = getAllMatchResults()

    #fixtures = getSeason(df, '24/25').reset_index(drop=True)
    #matches = getRound(fixtures, str(15))
    #print(fixtures)
    #matchFacts = matches[matches.columns.drop('rugbypassURL')]
    #print(matchFacts)
    match = df.iloc[-1].to_frame().T
    print(match)
    matchFacts = match[match.columns.drop('rugbypassURL')]
    url = 'https://www.rugbypass.com/live/exeter-chiefs-vs-gloucester/?g=943614'
    print(url)
    

    lastestData, statsData = scrapeData(url)
    #print(lastestData, statsData)
    lastestDf = createLatestDf(lastestData)
    statsDf = createStatsDf(statsData)
    matchResult = matchFacts.iloc[-1].to_frame().T
    frames = [matchResult, lastestDf, statsDf]
    mergerdMatch = mergeDf(frames)
    try:
        mergerdMatch.to_csv('premiershipMatchData22-25.csv', mode = 'a', index = False, header=False)
    except FileNotFoundError:
        return

    # for i in range(len(match)):
    #     url = match['rugbypassURL']
    #     if type(url) == str:
    #         try:
    #             lastestData, statsData = scrapeData(url)
    #             #print(lastestData, statsData)
    #             lastestDf = createLatestDf(lastestData)
    #             statsDf = createStatsDf(statsData)
    #             matchResults = matchFacts.iloc[i].to_frame().T
    #             #fixtures[fixtures.columns.drop('rugbypassURL')].loc[i].to_frame().T
    #             # print(matchResults)
    #             frames = [matchResults, lastestDf, statsDf]
    #             mergerdMatch = mergeDf(frames)
    #             try:
    #                mergerdMatch.to_csv('premiershipMatchData22-25.csv', mode = 'a', index = False, header=False)
    #             except FileNotFoundError:
    #                return
    #         except:
    #             continue
    #     #time out used to prevent heavy spam 
    #     time.sleep(3)
    return 
if __name__ == '__main__':
    main()