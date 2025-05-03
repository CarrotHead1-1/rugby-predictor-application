
import pandas as pd
import os 
import pickle
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from features import features
from randomForest import RandomForest


rf = RandomForest(numTrees=10)

#directory paths


def datasetSetup():

    df = features()

    df = encodeValues(df)
    df = removeMissing(df)

    X, y = selectFeatures(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

    #train the rf model
    rf.fit(X_train, y_train)

    #test model
    y_pred = rf.predict(X_test)

    print("Accuracy", accuracy_score(y_test, y_pred))
    print("Classification Report: \n", classification_report(y_test, y_pred))

    featureNames = df[df.columns.drop(['HomeTeam', 'AwayTeam', 'Season', 'Round','Team_1', 'Team_2', 'Result', 'Target'])]
    importantFeatures = rf.importance()
    linked = {featureNames.columns[i]: score for i, score in importantFeatures.items()}

    for feature, score in sorted(linked.items(), key=lambda x: x[1], reverse=True):
        print(f"{feature}: {score:.4f}")

    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)
    picklePath = os.path.join(static_dir, "rf_model.pkl")

    with open(picklePath, "wb") as f:
        pickle.dump(rf, f)

def removeMissing(df):
    return df.dropna()

def selectFeatures(df):
    #print(df.columns)
    #gets all the features in the dataset
    features = df[df.columns.drop(['HomeTeam', 'AwayTeam', 'Season', 'Round','Team_1', 'Team_2', 'Result', 'Target'])].values
    #print(features)
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