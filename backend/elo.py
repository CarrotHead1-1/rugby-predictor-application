import matplotlib.pyplot as plt
import pandas as pd 
import os

eloRatings= {}
history = {}

def getElo(team):
    return eloRatings.get(team, 1500)

def updateElo(home, away, homeScore, awayScore):
    homeElo = getElo(home)
    awayElo = getElo(away)

    #works out which team won or if a draw occurs
    if homeScore > awayScore:
        result = 1
    elif awayScore > homeScore:
        result = 0
    else:
        result = 0.5

    # Constant elo change
    K = 35
    expectedResult = 1 / (1 + 10 ** ((awayElo - homeElo) / 400))

    #update ratings
    eloRatings[home] = homeElo + K * (result - expectedResult)
    eloRatings[away] = awayElo + K * ((1 - result) - (1 - expectedResult))
    
    for team, rating in [(home, eloRatings[home]), (away, eloRatings[away])]:
        if team not in history:
            history[team] = []
        history[team].append(rating)

def getHistroy():
    return history

def processMatchElo(df):
    global eloRatings, history
    eloRatings = {}
    history = {}

    matchELo = []

    for _, row in df.iterrows():

        homeElo = getElo(row["HomeTeam"])
        awayElo = getElo(row["AwayTeam"])

        matchELo.append({
            "HomeTeam" : row["HomeTeam"],
            "AwayTeam" : row["AwayTeam"],
            "HomeElo" : homeElo,
            "AwayElo" : awayElo,
            "EloDiff" : homeElo - awayElo
        })
        
        updateElo(
            home=row['HomeTeam'],
            away=row['AwayTeam'],
            homeScore=row['HomeScore'],
            awayScore=row['AwayScore']
        )

    return pd.DataFrame(matchELo)

def plotEloChange(teams=None):


    plt.figure(figsize=(12, 6))

    if teams is None:
        teams = list(history.keys())

    for team in teams:
        games = list(range(1, len(history[team]) + 1))
        plt.plot(games, history[team], label = team)
    
    plt.xlabel('Games Played')
    plt.ylabel('Elo Rating')
    plt.title("Elo Rating across Games Played")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    #saving the graph image
    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)
    path = os.path.join(static_dir, 'eloGraph.png')
    plt.savefig(path)
    
    plt.close()
    return path
