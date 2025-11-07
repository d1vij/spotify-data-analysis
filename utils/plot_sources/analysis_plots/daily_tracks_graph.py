import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

from utils.filters import Filters

def daily_tracks_graph(df: pd.DataFrame, _ax=None):
    fig = None
    # daily number of songs listend to
    daywise_plays_df = df[["ts", "ms_played"]].copy(True)

    # filtering out skipped tracks
    daywise_plays_df = daywise_plays_df[daywise_plays_df["ms_played"] >= 1e4]
    daywise_plays_df.sort_values("ts", inplace=True)
    dates = daywise_plays_df["ts"].apply(
        lambda ts: datetime.strftime(ts, "%Y-%m-%d")
    )
    datewise_track_count_ser = dates.groupby(dates).count()
    datewise_track_count_ser = Filters.rows_gt(0, datewise_track_count_ser);
    min_date = dates.min()
    max_date = dates.max()
    if not max_date >= min_date:
        raise RuntimeError(
            f"Start date {min_date} and End date {max_date} dont make sense"
        )  # accounting the edge case when user no listening history

    __x = pd.to_datetime(datewise_track_count_ser.index)
    __y = datewise_track_count_ser.values

    if _ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))
    else:
        ax = _ax

    sns.scatterplot(
        x=__x,
        y=__y,
        hue=datewise_track_count_ser.values,
        ax=ax,
        palette="coolwarm",
        marker="o",
        size=60,
    )
    date_ticks = pd.date_range(
        start=min_date, end=max_date, periods=7, inclusive="both"
    )
    ax.set_xticks(
        [d.strftime(format="%Y-%m-%d") for d in date_ticks],
        labels=[d.strftime("%b %Y") for d in date_ticks],
    )
    ax.set_title("Number of tracks played daily")
    sns.despine()
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=True)

    if fig is not None:
        fig.tight_layout()

    if _ax is None:
        plt.show()