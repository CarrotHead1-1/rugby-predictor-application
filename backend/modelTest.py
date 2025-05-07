
import json
import pandas as pd
import os 
import pickle
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from features import features
from randomForest import RandomForest


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data", "matchResults2018-2025.csv")
STATIC_PATH = os.path.join(BASE_PATH, "static")
df1 = pd.read_csv(DATA_PATH)
df1 = df1[df1.columns.drop('rugbypassURL')]

df2 = pd.read_csv(os.path.join(BASE_PATH, "data", "premiershipMatchData22-25.csv"))

rf = RandomForest(numTrees=10, maxDepth=10, minSamples=2)

def datasetSetup():

    df, _, _ = features(df1, df2)
    
    df = encodeValues(df)
    df = removeMissing(df)  
    
    X, y = selectFeatures(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

    #train the rf model
    rf.fit(X_train, y_train)

    #test model
    y_pred = rf.predict(X_test)

    print("Accuracy", accuracy_score(y_test, y_pred))
    print("Classification Report: \n", classification_report(y_test, y_pred, output_dict=True))

    modelAccuracy = accuracy_score(y_test, y_pred)
    modelReport = classification_report(y_test, y_pred)

    accuracyReport = {
        "modelAccuracy": modelAccuracy,
        "classificationReport": modelReport
    }

    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)
    picklePath = os.path.join(static_dir, "rf_model.pkl")
    accuracyPath = os.path.join(static_dir, "rf_accuracyReport.json")
    with open(picklePath, "wb") as f:
        pickle.dump(rf, f)

    with open(accuracyPath, "w") as f:
        json.dump(accuracyReport, f, indent=4)

def removeMissing(df):
    return df.dropna()

def selectFeatures(df):
    
    #gets all the features in the dataset
    features = df[df.columns.drop(['HomeTeam', 'AwayTeam', 'Season', 'Round','Team_1', 'Team_2', 'Result', 'Target'])].values
    label = df["Target"].values

    return features, label



    #groups of features - used in testing
    # setPiece = ["Home Scrums", "Away Scrums", "Home Scrum Wins", "Away Scrum Wins", "Home Lineouts" ,"Away Lineouts", "Home Lineout Wins %", "Away Lineout Wins %", "Home Restarts Received", "Away Restarts Received", "Home Maul Success", "Away Mail Sucess"]
    # discipline = ["Home Penalties Conceded", "Away Penalties Conceded", "Home Yellow Cards", "Away Yellow Cards", "Home Red Cards", "Away Red Cards"]
    # tackles = ["Home Tackles Made", "Away Tackles Made", "Home Dominate Tackles", "Away Dominate Tackles", "Home Tackles Missed", "Away Tackles Missed", "Home Tackle Completion", "Away Tackle Completion"]
    # rucks = ["Home 0-3s Ruck Speed","Away 0-3s Ruck Speed","Home 3-6s Ruck Speed","Away 3-6s Ruck Speed","Home 6s+ Ruck Speed", "Away 6s+ Ruck Speed", "Home Rucks Won", "Away Rucks Won"]
    # attck = ["Home Tries", "Away Tries", "Home Conversions","Away Conversions", "Home Line Breaks", "Away Line Breaks","Home Metres Gained", "Away Metres Gained", "Home Carries", "Away Carries", "Home Post Contact Metres", "Away Post Contact Metres"
    #          , "Home 22m Entries", "Home 22m Conversions", "Away 22m Entries", "Away 22m Conversions"]
    # territoyAndPocession = ["Territory Home Try-Line - 22m","Territory Home 22m - 50m","Territory Away 22m - 50m","Territory Away Try-Line - 22m","Home Territory","Away Territory",
    #                         "Home Possessions Try Line - 22m","Home Possession 22m - 50m","Home Possession opp 50m - 22m", "Home Possession opp 22m - Try Line",
    #                         "Away Possessions Try Line - 22m","Away Possession 22m - 50m","Away Possession opp 50m - 22m", "Away Possession opp 22m - Try Line"]
    # defence = ["Home Turnovers Won", "Away Turnovers Won", "Home Tackle Turnovers", "Away Tackle Turnovers", "Home Offloads Allowed", "Away Offloads Allowed"]
    # kicking = ["Home Kicks", "Away Kicks", "Home Drop Goals", "Away Drop Goals", "Home Penalty Goals", "Away Penalty Goals"]
    # selected = attck + defence + tackles + kicking
    #features = df[selected].values
    #print(features)

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