import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

import os
import sys

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

innings_data = pd.read_csv(parent_directory / "data/innings.csv")

# sets custom colors
custom_palette = sns.color_palette("pastel", n_colors=3)

# Generates plots
ax = sns.countplot(
    data=innings_data,
    x="inning",
    hue="player_name",
    alpha=0.8,
    palette=custom_palette,
)
# adds customizations
ax.set(
    title="Innings in which an ABS challenge occurred \n Data as of 5/31:",
    xlabel="Inning",
    ylabel="# of Occurrences",
)
plt.legend(fontsize="medium", title="player", title_fontsize="7")
# Displays plot
plt.show()
