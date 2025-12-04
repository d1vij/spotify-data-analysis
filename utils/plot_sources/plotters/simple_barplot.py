import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def simple_barplot(y: pd.Series, title: str, xlabel, ylabel, _ax=None):
    if _ax is None:
        fig, ax = plt.subplots(figsize=(7, 5))
    else:
        ax = _ax

    sns.barplot(x=y.index, y=y.values, palette="pastel", hue=y.index, ax=ax)  # type: ignore
    for container in ax.containers:
        ax.bar_label(container)  # type: ignore

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.grid(linestyle=":", axis="y")

    sns.despine(top=True, right=True)
    if ax is None:
        plt.show()
