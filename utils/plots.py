import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from typing import cast
from .filters import *
from .smoothen import *
from wordcloud import WordCloud
import squarify

class Plots:
    """All methods return a figure object"""
    
    
    
    @staticmethod
    def plot_squarify(ser: pd.Series, title):
        plt.figure(figsize=(11, 11))
        squarify.plot(
            sizes=ser.values,
            label=ser.index,
            alpha=0.8,
            color=sns.color_palette("coolwarm_r", len(ser)),
        )
        sns.despine(top=True, bottom=True, right=True, left=True)

        plt.xticks([], labels=[])
        plt.yticks([], labels=[])
        
        plt.title(title, fontsize=23)
        plt.tight_layout()

        return plt.figure()
        # plt.show()

    @staticmethod
    def simple_barplot(y: pd.Series, title: str, xlabel, ylabel):
        plt.figure(figsize=(7, 5))

        ax = sns.barplot(x=y.index, y=y.values, palette="pastel", hue=y.index)  # type: ignore

        for container in ax.containers:
            plt.bar_label(container)  # type: ignore
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.grid(linestyle=":", axis="y")

        sns.despine(top=True, right=True)
        plt.tight_layout()
        return plt.figure()

    @staticmethod
    def daily_tracks_graph(df: pd.DataFrame):
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
        if(not max_date >= min_date):
            raise RuntimeError(f"Start date {min_date} and End date {max_date} dont make sense") # mainly for the particular edge case

        __x = pd.to_datetime(datewise_track_count_ser.index)
        __y = datewise_track_count_ser.values

        
        fig, ax = plt.subplots()
        sns.scatterplot(
            x=__x,
            y=__y,
            hue=datewise_track_count_ser.values,
            ax=ax,
            palette="coolwarm",
            marker=".",
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
        
        fig.tight_layout()
        return fig

    @staticmethod
    def track_playtime_kde_dist(df: pd.DataFrame):
        track_playtime_ser = df["ms_played"].copy(True)
        track_playtime_ser = track_playtime_ser.apply(lambda ts: int(ts) / 6e4).round(3)

        under_min = cast(pd.Series, Filters.rows_lteq(1, track_playtime_ser))

        track_playtime_ser = cast(pd.Series, Filters.rows_gteq(1, track_playtime_ser)) # only for intellisence
        track_playtime_ser = cast(pd.Series, Filters.rows_lteq(10, track_playtime_ser))

        fig, ax = plt.subplots(2,1, figsize=(10,7))

        # Plotting the KDE distribution of track playtimes
        # To prevent skewing of data, playtimes between 1 and 10minutes are only considered
        # since a lot of tracks with playtime under a minute could be skipped tracks and
        # the tracks over 10 minutes might be scarce but widely spread
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

        fig.tight_layout()
        return fig

        
    @staticmethod
    def daily_listening_activity(df: pd.DataFrame):
        hour_df = df.copy()
        hour_df["hour"] = hour_df["ts"].dt.hour  # much simpler than strftime
        hour_wise_count = hour_df.groupby("hour").size()

        # Ensure all 24 hours are present
        hour_wise_count = hour_wise_count.reindex(range(24), fill_value=0)

        total_tracks = hour_wise_count.sum()
        smoothened = smoothen(hour_wise_count, 1000)

        # daytime splits
        late_nights = smoothened[(smoothened.index > 0) & (smoothened.index <= 4)]
        mornings = smoothened[(smoothened.index > 4) & (smoothened.index <= 11)]
        afternoons = smoothened[(smoothened.index > 11) & (smoothened.index <= 16)]
        evenings = smoothened[(smoothened.index > 16) & (smoothened.index <= 20)]
        nights = smoothened[(smoothened.index > 20) & (smoothened.index < 24)]

        daytimes = [late_nights, mornings, afternoons, evenings, nights]
        daytime_names = ["Late Nights", "Mornings", "Afternoons", "Evenings", "Nights"]
        daytime_colors = ["#2c3e50", "#f1c40f", "#3498db", "#e67e22", "#8e44ad"]


        fig, ax = plt.subplots()

        for idx, daytime_ser in enumerate(daytimes):
            ax.fill_between(
                daytime_ser.index,
                0,
                daytime_ser.values, #type: ignore
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
        return fig
    
    @staticmethod
    def double_lineplot(x1, y1, label_1, color_1, x2, y2, label_2, color_2, * , x_ticks, x_tick_label ):
        fig, ax = plt.subplots(1, 1, figsize=(10, 4))
        ax.axhline(y1.max(), color="#5EABD6", alpha=0.5, linestyle='--')
        ax.axhline(y2.max(), color="#EF5A6F", alpha=0.5, linestyle='--')

        sns.lineplot(
            x=x1,
            y=y1,
            label=label_1,
            color=color_1,
            marker=".",
            ax=ax
        )
        sns.lineplot(
            x=x2,
            y=y2,
            label=label_2,
            color=color_2,
            marker=".",
            ax=ax
        )
        dates  = copy["ts"].apply(lambda ts: datetime.strftime(ts, "%Y-%m-%d"))
        min_date = dates.min()
        max_date = dates.max()

        date_ticks = pd.date_range(start=min_date, end=max_date, periods=7, inclusive="both")

        if(x_ticks):
            if(not x_tick_label): raise RuntimeError("X tick labels must be passed if ticks are passed")
            ax.set_xticks(x_ticks, x_tick_label)

        
        
        ax.legend(
            loc="upper left",
        )
        sns.despine()

        plt.xlabel("")
        plt.ylabel("")
        plt.title("Variablilty in artists and tracks")
        plt.tight_layout()
        plt.show()