
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

    for _, row in df.iterrows():
        updateH2H(
            home=row['HomeTeam'],
            away=row['AwayTeam'],
            homeScore=row['HomeScore'],
            awayScore=row['AwayScore']
        )
    return h2h

if __name__ == "__main__":
    print(h2h)
    results = processMatchH2H()
    print(results)
        