# https://github.com/d1vij/spotify-data-analysis/tree/ffc4be093155d40d2be87b00373c749324317c68


from datetime import datetime
from typing import cast

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import seaborn as sns
import squarify

from .filters import Filters
from .smoothen import smoothen
from .series_textwrap import index_wrap
from .series_textellipses import index_ellipses


class Plots:
    """All methods return a figure object"""

    @staticmethod
    def plot_squarify(ser: pd.Series, title, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))

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

        if ax is None:
            plt.show()

    @staticmethod
    def simple_barplot(y: pd.Series, title: str, xlabel, ylabel, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(x=y.index, y=y.values, palette="pastel", hue=y.index)  # type: ignore

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

    @staticmethod
    def daily_tracks_graph(df: pd.DataFrame, _ax=None):
        fig = None
        # daily number of songs listend to
        daywise_plays_df = df[["ts", "ms_played"]].copy(True)

        # filtering out skipped tracks
        daywise_plays_df = daywise_plays_df[daywise_plays_df["ms_played"] >= 3e4]
        daywise_plays_df.sort_values("ts", inplace=True)
        dates = daywise_plays_df["ts"].apply(
            lambda ts: datetime.strftime(ts, "%Y-%m-%d")
        )
        datewise_track_count_ser = dates.groupby(dates).count()

        min_date = dates.min()
        max_date = dates.max()
        if not max_date >= min_date:
            raise RuntimeError(
                f"Start date {min_date} and End date {max_date} dont make sense"
            )  # mainly for the particular edge case

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

    @staticmethod
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

    @staticmethod
    def daily_listening_activity(df: pd.DataFrame, _ax=None):
        fig = None

        hour_df = df.copy()
        hour_df["hour"] = hour_df[
            "ts"
        ].dt.hour  # much simpler than filtering using date.strftime,
        # since values in df.ts are already datetime objects

        # Total minutes played in a particular hour
        # SQL Logic would be -> select hour, sum(ms_played) / 60000
        #   from df
        #   group by hour
        hour_wise_count = hour_df.groupby("hour")["ms_played"].sum() / 60000

        # Ensure all 24 hours are present, fills the missing one with 0s
        hour_wise_count = hour_wise_count.reindex(range(24), fill_value=0)

        # Smoothening out the data so that the graph is continous and smooth by interpolating the data
        smoothened = smoothen(hour_wise_count, 1000)

        # Daytime splits series
        late_nights = smoothened[(smoothened.index > 0) & (smoothened.index <= 4)]
        mornings = smoothened[(smoothened.index > 4) & (smoothened.index <= 11)]
        afternoons = smoothened[(smoothened.index > 11) & (smoothened.index <= 16)]
        evenings = smoothened[(smoothened.index > 16) & (smoothened.index <= 20)]
        nights = smoothened[(smoothened.index > 20) & (smoothened.index < 24)]

        daytimes = [late_nights, mornings, afternoons, evenings, nights]
        daytime_names = ["Late Nights", "Mornings", "Afternoons", "Evenings", "Nights"]
        daytime_colors = ["#2c3e50", "#f1c40f", "#3498db", "#e67e22", "#8e44ad"]

        if _ax is None:
            fig, ax = plt.subplots(figsize=(10, 4))
        else:
            ax = _ax

        for idx, daytime_ser in enumerate(daytimes):
            ax.fill_between(
                daytime_ser.index,
                0,
                daytime_ser.values,  # type: ignore
                alpha=0.25,
                color=daytime_colors[idx],
            )
            sns.lineplot(
                x=daytime_ser.index,
                y=daytime_ser.values,
                ax=ax,
                label=daytime_names[idx],
                color=daytime_colors[idx],
            )
            ax.vlines(
                daytime_ser.index.max(),
                0,
                daytime_ser.iat[-1],
                linestyle="solid",
                color="000",
                alpha=0.125,
            )

        ax.set_xticks(range(24))
        ax.set_xlabel("Hour")
        ax.set_ylabel("Minutes listened")
        ax.set_title("Listening activity throughout day")
        ax.set_ylim(0, None)
        sns.despine()

        if _ax is None:
            plt.show()

    @staticmethod
    def double_lineplot(
        x1,
        y1,
        label_1,
        color_1,
        x2,
        y2,
        label_2,
        color_2,
        *,
        x_ticks,
        x_tick_label,
        _ax,
    ):
        fig = None

        if _ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(10, 4))
        else:
            ax = _ax

        ax.axhline(y1.max(), color="#5EABD6", alpha=0.5, linestyle="--")
        ax.axhline(y2.max(), color="#EF5A6F", alpha=0.5, linestyle="--")

        sns.lineplot(x=x1, y=y1, label=label_1, color=color_1, marker=".", ax=ax)
        sns.lineplot(x=x2, y=y2, label=label_2, color=color_2, marker=".", ax=ax)

        if x_ticks:
            if not x_tick_label:
                raise RuntimeError("X tick labels must be passed if ticks are passed")
            ax.set_xticks(x_ticks, x_tick_label)

        ax.legend(
            loc="upper left",
        )
        sns.despine()

        plt.xlabel("")
        plt.ylabel("")
        plt.title("Variablilty in artists and tracks")

        if fig is not None:
            fig.tight_layout()

        if _ax is None:
            plt.show()

    @staticmethod
    def variability_in_artists_and_tracks(df: pd.DataFrame, _ax=None):
        fig = None

        # Number of Unique artists vs Unique tracks listend each month
        # Plots monthly data for each month from first listened track to latest track

        copy = df[
            ["ts", "master_metadata_album_artist_name", "master_metadata_track_name"]
        ].copy(True)

        # Converts the timestamp into monthly periods
        # For example, "2021-08-11 09:22:28+00:00" would get converted into "2021-08"
        copy["month"] = copy["ts"].dt.tz_convert(None).dt.to_period("M")

        copy.sort_values("ts", inplace=True, ascending=True)

        # df.nunique() gives the count of unique values
        monthwise_unique_artists_count = copy.groupby("month")[
            "master_metadata_album_artist_name"
        ].nunique()

        monthwise_unique_track_count = copy.groupby("month")[
            "master_metadata_track_name"
        ].nunique()

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

    @staticmethod
    def analysis_per_artist(frame: pd.DataFrame, artist: str):
        if artist not in frame["master_metadata_album_artist_name"].values:
            raise ValueError(f"Artist {artist} is not in data")

        artist_frame = frame[frame["master_metadata_album_artist_name"] == artist].copy(
            True
        )
        # grouped = artist_frame.groupby("master_metadata_album_artist_name")
        # changing ts to year
        artist_frame["year"] = artist_frame["ts"].apply(
            lambda ts: datetime.strftime(ts, "%Y")
        )

        # Setting up plot grid
        fig = plt.figure(figsize=(18, 20), constrained_layout=True)

        grid = fig.add_gridspec(
            4, 2, height_ratios=[2.5, 1, 1, 1.5], hspace=0.4, wspace=0.3
        )

        # 1x2
        ax1 = fig.add_subplot(grid[0, :])

        # 1x1
        ax2 = fig.add_subplot(grid[1, 0])

        # 1x1
        # Currently empty
        ax3 = fig.add_subplot(grid[1, 1])

        # 1x1

        ax4 = fig.add_subplot(grid[2, 0])
        ax5 = fig.add_subplot(grid[2, 1])
        ax6 = fig.add_subplot(grid[3, :])

        # Top 50 played tracks
        played_track_count = (
            artist_frame.groupby("master_metadata_track_name")
            .size()
            .sort_values(ascending=False)
        )

        index_wrap(played_track_count, 12)
        index_ellipses(played_track_count, 22)

        Plots.plot_squarify(
            played_track_count[:50], f"Fifty most played tracks by {artist}", ax1
        )

        # Year wise play time
        yearwise_playtime = artist_frame.groupby("year").size()
        Plots.simple_barplot(
            yearwise_playtime,
            f"Tracks played in a particular year by {artist}",
            "Year",
            "Play count",
            ax2,
        )

        # fig, ax = plt.subplots(2, 2, figsize=(15,7.5))

        fig.suptitle("Track analysis for " + artist, fontsize=23)

        Plots.daily_tracks_graph(artist_frame, ax4)
        Plots.track_playtime_kde_dist(artist_frame, [ax5, ax3])  # type: ignore
        Plots.daily_listening_activity(artist_frame, ax6)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def top_n_artists_by_playtime(df: pd.DataFrame, n: int):
        # Top artists by playtime
        copy = df.copy(True)
        grouped_by_artist_name = copy.groupby(copy["master_metadata_album_artist_name"])
        time_listend = grouped_by_artist_name["ms_played"].sum()
        time_listend = time_listend[time_listend != 0]
        time_listend.sort_values(ascending=False, inplace=True)
        time_listend_mins = time_listend.div(6e4)
        time_listend_mins = cast(pd.Series, Filters.rows_gt(1, time_listend_mins))
        index_wrap(time_listend_mins, 10)
        Plots.plot_squarify(
            time_listend_mins[:n], f"Top {n} played artists by listening minutes"
        )

    @staticmethod
    def top_n_tracks_by_playcount(df: pd.DataFrame, n: int):
        most_played_tracks = df.groupby(df["master_metadata_track_name"])[
            "master_metadata_track_name"
        ].count()
        most_played_tracks.sort_values(ascending=False, inplace=True)
        index_wrap(most_played_tracks, 10)
        Plots.plot_squarify(most_played_tracks[:n], f"{n} Most played tracks")

    @staticmethod
    def yearwise_listening_minutes(df: pd.DataFrame):
        copy = df.copy(True)
        copy["ts"] = copy["ts"].dt.year
        yearwise_playtime = copy.groupby("ts")["ms_played"].sum() / 60000
        Plots.simple_barplot(
            yearwise_playtime, "Yearwise playtime in minutes", "Year", "Minutes Played"
        )
