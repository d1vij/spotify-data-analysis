import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from utils.smoothen import smoothen


# Generates a linechart with total minutes of track playtime for each part of the day
# Parts of day is divided based on (24) hours, as follow
# Late Night: 0 -> 4 th hour
# Morning: 4 -> 11
# Afternoons: 11 -> 16
# Evenings: 16 -> 20
# Nights: 20 -> 24
def daily_listening_activity(df: pd.DataFrame, _ax=None):
    fig = None

    hour_df = df.copy()
    hour_df["hour"] = hour_df["ts"].dt.hour  # much simpler than filtering using date.strftime,
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
        fig, ax = plt.subplots(figsize=(10, 2))
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
