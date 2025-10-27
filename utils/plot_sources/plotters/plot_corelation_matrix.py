import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_corelation_matrix(
    df: pd.DataFrame,
    title: str,
    x_label: str,
    y_label: str,
    *,
    ax=None
):
    if (ax is None):
        fig, ax = plt.subplots(figsize=(7, 5))
    
    ax.set_title(
        "Co-occurance plot - Number of times person A got voted when person B was voted",
        size=16,
    )
    sns.heatmap(
        df,
        cmap="viridis",
        vmin=0,
        annot=True,
        ax=ax,
        fmt=".0f",
        cbar_kws={"label": "Count"},
    )
    ax.set_ylabel(y_label, size=12)
    ax.set_xlabel(x_label, size=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)


    if(ax is None):
        plt.show()
