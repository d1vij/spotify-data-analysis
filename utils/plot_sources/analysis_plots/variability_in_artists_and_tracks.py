import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def variability_in_artists_and_tracks(df: pd.DataFrame, _ax=None):
    fig = None

    # Number of Unique artists vs Unique tracks listend each month
    # Plots monthly data for each month from first listened track to latest track

    copy = df[["ts", "master_metadata_album_artist_name", "master_metadata_track_name"]].copy(True)

    # Converts the timestamp into monthly periods
    # For example, "2021-08-11 09:22:28+00:00" would get converted into "2021-08"
    copy["month"] = copy["ts"].dt.tz_convert(None).dt.to_period("M")

    copy.sort_values("ts", inplace=True, ascending=True)

    # df.nunique() gives the count of unique values
    monthwise_unique_artists_count = copy.groupby("month")["master_metadata_album_artist_name"].nunique()

    monthwise_unique_track_count = copy.groupby("month")["master_metadata_track_name"].nunique()

    # Concatenating the two series into one dataframe
    aggr = pd.concat(
        [monthwise_unique_artists_count, monthwise_unique_track_count],
        axis=1,  # 1, so as to join row wise
    )
    aggr["month-year"] = aggr.index.strftime("%b %Y")  # type:ignore
    aggr.rename(
        {
            "master_metadata_album_artist_name": "Artist Count",
            "master_metadata_track_name": "Track Count",
        },
        inplace=True,
        axis=1,
    )

    y1 = aggr["Artist Count"]
    y2 = aggr["Track Count"]

    if _ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    else:
        ax = _ax

    # Drawing horizontal lines on figure representing max peak of each plot
    ax.axhline(y1.max(), color="#5EABD6", alpha=0.5, linestyle="--")
    ax.axhline(y2.max(), color="#EF5A6F", alpha=0.5, linestyle="--")

    sns.lineplot(
        x=aggr["month-year"],
        y=y1,
        label=["Artist Count"],
        color="#5EABD6",
        marker=".",
        ax=ax,
    )
    sns.lineplot(
        x=aggr["month-year"],
        y=y2,
        label=["Track Count"],
        color="#EF5A6F",
        marker=".",
        ax=ax,
    )

    dates = copy["ts"].apply(lambda ts: datetime.strftime(ts, "%Y-%m-%d"))

    min_date = dates.min()
    max_date = dates.max()

    date_ticks = pd.date_range(
        start=min_date,
        end=max_date,
        freq="6ME",
        # periods=7,
        inclusive="left",
    )

    print(date_ticks)
    ax.set_xticks(
        date_ticks.strftime("%b %Y"),
        labels=[d.strftime("%b %Y") for d in date_ticks],
    )
    ax.legend(
        loc="upper right",
    )
    sns.despine()

    plt.xlabel("")
    plt.ylabel("Count")
    plt.title("Variability in artists and tracks")
    plt.tight_layout()

    if _ax is None:
        plt.show()
