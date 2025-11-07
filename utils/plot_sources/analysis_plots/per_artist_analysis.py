from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from utils.series_textwrap import index_wrap
from utils.series_textellipses import index_ellipses

from plotters.double_lineplot import double_lineplot
from plotters.simple_barplot import simple_barplot 
from plotters.plot_squarify import plot_squarify

from analysis_plots.daily_tracks_graph import daily_tracks_graph
from analysis_plots.track_playtime_kde_dist import track_playtime_kde_dist
from analysis_plots.daily_listening_activity import daily_listening_activity

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

    plot_squarify(
        played_track_count[:50], f"Fifty most played tracks by {artist}", ax1
    )

    # Year wise play time
    yearwise_playtime = artist_frame.groupby("year").size()
    simple_barplot(
        yearwise_playtime,
        f"Tracks played in a particular year by {artist}",
        "Year",
        "Play count",
        ax2,
    )

    # fig, ax = plt.subplots(2, 2, figsize=(15,7.5))

    fig.suptitle("Track analysis for " + artist, fontsize=23)

    daily_tracks_graph(artist_frame, ax4)
    track_playtime_kde_dist(artist_frame, [ax5, ax3])  # type: ignore
    daily_listening_activity(artist_frame, ax6)

    plt.tight_layout()
    plt.show()