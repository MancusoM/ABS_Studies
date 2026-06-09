import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import sys

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

catcher_data = pd.read_csv(parent_directory / "data/innings.csv")

def cleaning_data(catcher_data: pd.DataFrame) -> pd.DataFrame:
    """

    cleans data
        removes unnecessary cols
        changes delta_win_exp into Mets' delta win exp
        minor rounding

    :param catcher_data: raw df from savant search
    :return:
    """

    empty_list = []
    for _, i in catcher_data.iterrows():

        if i["home_team"] == "NYM":
            i["mets_win_expectancy"] = i["home_win_exp"]
        elif i["home_team"] != "NYM":
            i["mets_win_expectancy"] = i["home_win_exp"] * -1

        if i["mets_win_expectancy"] > 0:
            i["Team Projected to Win"] = "Mets"
        else:
            i["Team Projected to Win"] = "Opponent"

        dictionary = {
            "Mets_win_expectancy": i["mets_win_expectancy"],
            "Player": i["player_name"],
            "pitcher": i["pitcher"],
            "batter": i["batter"],
            "Team Projected to Win": i["Team Projected to Win"],
            "pitch_name": i["pitch_type"],
            "inning": i["inning"],
        }

        empty_list.append(dictionary)

    dataframe = pd.DataFrame(empty_list)
    dataframe["Mets_win_expectancy"] = round(dataframe["Mets_win_expectancy"] * 100, 4)
    return dataframe


dataframe = cleaning_data(catcher_data)

dataframe["Mets_win_expectancy"] = dataframe["Mets_win_expectancy"].apply(
    lambda x: x * -1 if x < 0 else x
)
print(dataframe.groupby("Player")["Mets_win_expectancy"].mean())

custom_palette = sns.color_palette()
# generates plot
ax = sns.swarmplot(
    data=dataframe,
    x="Player",
    y="Mets_win_expectancy",
    hue="Team Projected to Win",
    alpha=0.8,
    palette="deep",
)

# Customizations
plt.ylim(0, 100)
plt.axhline(50, color="red", linestyle="--", linewidth=1.5)
plt.axhline(40, color="green", linestyle="--", linewidth=1.5)
plt.axhline(60, color="green", linestyle="--", linewidth=1.5)
ax.tick_params(axis="y", labelrotation=45)

ax.set(
    title="[Mets Catchers]: \n Win Expectancy at Time of Mets Challenge \n ",
    xlabel="Catcher",
    ylabel="Mets' Win Expectancy \n At Time of Challenge",
)
ax.set_yticklabels(ax.get_yticklabels(), rotation=45)
# display plot
plt.show()
