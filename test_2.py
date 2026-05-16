from pybaseball import batting_stats_bref
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# get all of this season's batting data so far
data = batting_stats_bref()
print(data)

# mets_id_data = batter_data.query('home_team == "NYM" or away_team == "NYM"')
