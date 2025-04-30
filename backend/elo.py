
eloRatings= {}

def getElo(team):
    return eloRatings.get(team, 1500)

def updateElo(home, away, homeScore, awayScore):
    homeElo = getElo(home)
    awayElo = getElo(away)

    #print(f"{home} : {homeElo}, {away} : {awayElo}")
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
    #print(expectedResult)
    #update ratings
    eloRatings[home] = homeElo + K * (result - expectedResult)
    eloRatings[away] = awayElo + K * ((1 - result) - (1 - expectedResult))
    
    
def processMatchElo(df):

    for _, row in df.iterrows():
        updateElo(
            home=row['HomeTeam'],
            away=row['AwayTeam'],
            homeScore=row['HomeScore'],
            awayScore=row['AwayScore']
        )
        
    return eloRatings



if __name__ == '__main__':
    finalRatings = processMatchElo()

    print("final elo ratings")
    for team, rating in sorted(finalRatings.items(), key=lambda x: -x[1]):
        print(f"{team} : {round(rating, 2)}")