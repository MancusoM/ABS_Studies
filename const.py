from pybaseball import statcast
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# Pull Statcast data for the current MLB season
df = statcast(start_dt="2026-04-25", end_dt="2026-04-26", team="NYM")
print(df)

# Batter IDs -> team
batters = df[["batter", "home_team"]].dropna().drop_duplicates(subset=["batter"])
# Build dictionary
player_team_dict = {}

from pybaseball import batting_stats_bref

# get all of this season's batting data so far
data = batting_stats_bref()
print(data)

# retrieve data on the 2009 season

print(batters)

for _, row in batters.iterrows():
    player_team_dict["batter"] = row["home_team"]

data = pd.DataFrame(player_team_dict["batter"], player_team_dict["home_team"]).to_csv(
    "teams_players_mapping.csv"
)

"""
# Add batters
for _, row in batters.iterrows():
    player_team_dict[int(row["batter"])] = row["home_team"]

# Add pitchers
for _, row in pitchers.iterrows():
    player_team_dict[int(row["pitcher"])] = row["away_team"]

print(player_team_dict)
data = pd.DataFrame(player_team_dict,index=[0]).to_csv("teams_players_mapping.csv")
"""
