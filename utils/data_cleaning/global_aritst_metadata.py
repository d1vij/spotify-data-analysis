# Script responsible for cleaning the csv for artist metadata

if __name__ == "__main__":
    from os import path
    import pandas as pd

    # Original CSV
    # https://www.kaggle.com/datasets/harshdprajapati/worldwide-music-artists-dataset-with-image

    csv_path = path.abspath(path.join(__file__, "../../../ext_data/global_music_artists.csv"))
    # Only reading the required columns from the csv
    df = pd.read_csv(filepath_or_buffer=csv_path, usecols=["artist_name", "artist_genre", "country"])

    # Overwriting the original
    df.to_csv(csv_path, index=False)
