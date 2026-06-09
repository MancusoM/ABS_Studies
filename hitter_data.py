import pandas as pd

from pathlib import Path
import os
import sys
import pybaseball
from pybaseball import playerid_reverse_lookup, playerid_lookup, batting_stats_bref

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

batter_data = pd.read_csv(parent_directory / "data/batter_data.csv")

pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)

# get all of this season's batting data so far
id_data = batting_stats_bref()

merged_data = batter_data.merge(id_data, left_on="batter", right_on="mlbID")
merged_data["League"] = merged_data["Lev"].apply(lambda x: x.split("-")[1])


empty_list = []
for _, i in merged_data.iterrows():
    if i["home_team"] == "NYM":
        i["mets_win_expectancy"] = i["delta_home_win_exp"]
    elif i["home_team"] != "NYM":
        i["mets_win_expectancy"] = i["delta_home_win_exp"] * -1

    if "," in i["Tm"]:
        i["Tm"] = i["Tm"].split(",")[1]

    dictionary = {
        "Tm": i["Tm"],
        "Mets_win_expectancy": i["mets_win_expectancy"],
        "Player": i["player_name"],
        "pitcher": i["pitcher"],
        "batter": i["batter"],
        "delta_home_win_exp": i["delta_home_win_exp"],
        "League": i["League"],
        "game_date": i["game_date"],
        "pitch_name": i["pitch_type"],
    }

    empty_list.append(dictionary)

dataframe = pd.DataFrame(empty_list)

dataframe["Team"] = dataframe["Tm"] + " " + dataframe["League"]
dataframe["Mets_win_expectancy"] = dataframe["Mets_win_expectancy"] * 100

import matplotlib.pyplot as plt
import seaborn as sns

data_order = (
    dataframe.groupby("Player")["Mets_win_expectancy"]
    .mean()
    .sort_values(ascending=False)
    .index
)

Mets_win_expectancy = dataframe["Mets_win_expectancy"]

ax = sns.boxplot(
    data=dataframe,
    y="Player",
    x=Mets_win_expectancy,
    hue="Player",
    # palette=custom_colors,
    order=data_order,
)

import textwrap

# Example Seaborn Plot
labels = [
    textwrap.fill(str(label.get_text()), width=10) for label in ax.get_yticklabels()
]
ax.set_yticklabels(labels)


plt.axvline(0.000, color="black", linestyle="--", linewidth=1.5)

ax.set(
    title="[Mets Batters]: Win Percentage Added/Lost via ABS",
    ylabel="Batter",
    xlabel="Win Percentage Points Added/Lost via ABS",
)

plt.show()
