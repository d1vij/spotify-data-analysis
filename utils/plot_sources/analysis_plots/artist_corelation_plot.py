from itertools import combinations
import pandas as pd

def get_probability_matrix(df: pd.DataFrame):
    top_n = 25

    grouped = df.groupby("master_metadata_album_artist_name")
    time_listened = grouped["ms_played"].sum().sort_values(ascending=False)

    top_n_artists = df[df["master_metadata_album_artist_name"].isin(time_listened.index[:top_n])].copy()
    top_n_artists["date"] = top_n_artists["ts"].dt.date

    unique_artists = top_n_artists["master_metadata_album_artist_name"].unique()
    unique_dates = top_n_artists["date"].unique()

    co_occurance_matrix = pd.DataFrame(0, index=unique_artists, columns=unique_artists, dtype=int)

    for date in unique_dates:
        # Selecting the artists played in that day
        artists = top_n_artists.loc[top_n_artists["date"] == date, "master_metadata_album_artist_name"].unique()
        for name_A, name_B in combinations(artists, 2):
            co_occurance_matrix.at[name_A, name_B] += 1
            co_occurance_matrix.at[name_B, name_A] += 1  # symmetric

    
    # creating conditional probability matrix
    # conditional probabilty matrix is created by normalizing columns of co-occurance matrix
    # normalizing means dividing each row of co-occurance matrix by the total votes in that row
    # the matrix gives the probabilty of person b (x axis) being voted when person A (y axis) was voted
    probability_matrix = co_occurance_matrix.div(co_occurance_matrix.sum(axis=1), axis=0)
    print(probability_matrix)
    return probability_matrix
