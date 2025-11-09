import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from typing import cast
from datetime import datetime

from utils.filters import Filters


def track_playtime_kde_dist(df: pd.DataFrame, _ax: list[Axes] | None = None):
    fig = None
    track_playtime_ser = df["ms_played"].copy(True)
    track_playtime_ser = track_playtime_ser.apply(lambda ts: int(ts) / 6e4).round(3)

    # Dataframe rows who's playtime is under a minute
    under_min = cast(pd.Series, Filters.rows_lteq(1, track_playtime_ser))

    # Filtering rows whose playtime is over 1 minute
    track_playtime_ser = cast(
        pd.Series, Filters.rows_gteq(1, track_playtime_ser)
    )  # only for intellisence

    # Filtering rows whose playtime is under 10 minute
    track_playtime_ser = cast(pd.Series, Filters.rows_lteq(10, track_playtime_ser))

    if _ax is None:
        fig, ax = plt.subplots(2, 1, figsize=(10, 7))
    else:
        ax = _ax

    # TODO: Find some alternative for this
    ax = cast(list[Axes], ax)

    # Plotting the KDE distribution of track playtimes
    # To prevent skewing of data, playtimes between 1 and 10minutes are only considered
    # since a lot of tracks with playtime under a minute could be skipped tracks and
    # the tracks over 10 minutes might be scarce but widely spread in terms of playtimes

    # KDE Distribution of playtimes over a minute and under 10 minutes
    # Filled line plot
    sns.kdeplot(
        x=track_playtime_ser.values,
        alpha=0.25,
        fill=True,
        color="red",
        linestyle="",
        ax=ax[0],
    )

    ax[0].set_title("KDE distribution of track playtimes (over minute)")
    ax[0].axvline(
        track_playtime_ser.mean(),
        0,
        label="Mean",
        linestyle=":",
        color="000",
        alpha=0.5,
    )
    ax[0].legend()

    # KDE Distribution of playtimes under a minute
    # Filled line plot
    sns.kdeplot(
        x=under_min.values,
        alpha=0.25,
        fill=True,
        color="blue",
        linestyle="",
        ax=ax[1],
    )

    ax[1].set_title("KDE distribution of track playtimes (under minute)")
    ax[1].set_xlabel("Minutes")
    ax[1].axvline(
        under_min.mean(), 0, label="Mean", linestyle=":", color="000", alpha=0.5
    )
    ax[1].legend()

    sns.despine()

    if fig is not None:
        fig.tight_layout()

    if _ax is None:
        plt.show()
