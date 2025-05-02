
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from features import features
from randomForest import RandomForest


rf = RandomForest()


def datasetSetup():

    df = features()

    df = encodeValues(df)
    df = removeMissing(df)

    X, y = selectFeatures(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

    #train the rf model
    rf.fit(X_train, y_train)

    #test model
    y_pred = rf.predict(X_test)

    print("Accuracy", accuracy_score(y_test, y_pred))
    print("Classification Report: \n", classification_report(y_test, y_pred))


def removeMissing(df):
    return df.dropna()

def selectFeatures(df):
    #print(df.columns)
    features = df[["HomeElo", "AwayElo", "EloDiff", "Team_1_Wins", "Team_2_Wins", "Draws", "HomeTeamCoded", "AwayTeamCoded"]].values
    label = df["Target"].values

    return features, label

def encodeValues(df):
    #encode features such as team names and result
    teamCodes = pd.Categorical(
        pd.concat([df["HomeTeam"], df["AwayTeam"]])
        ).categories
    df["HomeTeamCoded"] = pd.Categorical(df["HomeTeam"], categories=teamCodes).codes
    df["AwayTeamCoded"] = pd.Categorical(df["AwayTeam"], categories=teamCodes).codes

    resultCodes = {"HomeWin" : 2, "Draw" : 1, "AwayWin" : 0} 
    df["Target"] = (df["Result"].map(resultCodes))

    return df



if __name__ == "__main__":
    datasetSetup()