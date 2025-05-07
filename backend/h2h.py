
import pandas as pd

h2h = {}

def getH2H(teams):
    return h2h.get(teams, {"Team_1_Wins" : 0, "Team_2_Wins" : 0, "Draws" : 0})

def updateH2H(home, away, homeScore, awayScore):
    
    teams = tuple(sorted([home, away]))
    stats = getH2H(teams)
    #update h2h results
    if homeScore > awayScore:
        stats["Team_1_Wins"] += 1
    elif awayScore > homeScore:
        stats["Team_2_Wins"] += 1
    else:
        stats["Draws"] += 1

    h2h[teams] = stats


def h2hResults():
    return {f"{team1} vs {team2}": stats for (team1, team2), stats in h2h.items()}

def processMatchH2H(df):
    global h2h
    h2h = {}

    matchH2H = []

    for _, row in df.iterrows():

        teams = tuple(sorted([row["HomeTeam"], row["AwayTeam"]]))
        currentH2H = getH2H(teams)
        
        matchH2H.append({
            "HomeTeam" : row["HomeTeam"],
            "AwayTeam" : row["AwayTeam"],
            "Team_1"  : teams[0],
            "Team_2" : teams[1],
            "Team_1_Wins" : currentH2H["Team_1_Wins"],
            "Team_2_Wins" : currentH2H["Team_2_Wins"],
            "Draws" : currentH2H["Draws"]

        })

        updateH2H(
            home=row['HomeTeam'],
            away=row['AwayTeam'],
            homeScore=row['HomeScore'],
            awayScore=row['AwayScore']
        )

    return pd.DataFrame(matchH2H)