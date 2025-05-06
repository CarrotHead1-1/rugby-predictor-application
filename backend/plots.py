import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os 
from features import features

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data", "matchResults2018-2025.csv")
STATIC_PATH = os.path.join(BASE_PATH, "static")
df1 = pd.read_csv(DATA_PATH)
df1 = df1[df1.columns.drop('rugbypassURL')]

df2 = pd.read_csv(os.path.join(BASE_PATH, "data", "premiershipMatchData22-25.csv"))

# Combine the data
df = features(df1, df2)

# Create a Result column (assuming Home Score and Away Score are present)
df['Result'] = df.apply(lambda row: 'Home Win' if row['HomeScore'] > row['AwayScore'] 
                                     else ('Away Win' if row['HomeScore'] < row['AwayScore'] 
                                           else 'Draw'), axis=1)

# Print the first few rows to check the data
print(df.head())

# Select the columns for pairplot
selected = ["Home Tries", "Away Tries", "Home Conversions", "Away Conversions", 
            "Home Territory", "Away Territory",
            "Home Possession", "Away Possession", "Home Passes", "Away Passes", 
            "Home Penalties Conceded", "Away Penalties Conceded", "Home Tackle Completion",
            "Away Tackle Completion", "Home Metres Gained", "Away Metres Gained",
            "Result"]

# Filter the selected columns
cols = df[selected]

# Create the pairplot with 'Result' as hue for coloring the points
sns.pairplot(cols, hue='Result')


#saving the graph image
static_dir = os.path.join(os.getcwd(), "static")
os.makedirs(static_dir, exist_ok=True)
path = os.path.join(static_dir, 'pairsplot.png')
plt.savefig(path)