import pandas as pd
import seaborn as sns
import squarify
import matplotlib.pyplot as plt


def plot_squarify(ser: pd.Series, title, _ax=None):
    if _ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    else:
        ax = _ax

    squarify.plot(
        sizes=ser.values,
        label=ser.index,
        alpha=0.8,
        color=sns.color_palette("coolwarm_r", len(ser)),
        ax=ax,
    )

    sns.despine(top=True, bottom=True, right=True, left=True, ax=ax)

    ax.set_xticks([], labels=[])
    ax.set_yticks([], labels=[])

    ax.set_title(title, fontsize=23)

    if _ax is None:
        plt.show()
