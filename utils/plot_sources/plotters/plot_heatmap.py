import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_heatmap(df: pd.DataFrame, title: str, x_label: str, y_label: str, *, _ax=None, _fmt=".0f"):
    if _ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        ax = _ax
    ax.set_title(
        title,
        size=16,
    )
    sns.heatmap(
        df,
        cmap="viridis",
        vmin=0,
        annot=True,
        ax=ax,
        fmt=_fmt,
        cbar_kws={"label": "Count"},
    )

    ax.set_ylabel(y_label, size=12)
    ax.set_xlabel(x_label, size=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    if _ax is None:
        plt.show()
