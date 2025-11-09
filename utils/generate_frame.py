from os.path import isfile, abspath
import pandas as pd

from utils.process_zip import SongAttributes
from utils.process_zip import process_zip

DEBUG = True


# Asks user for the filepath of the spotify data zip file
# and processes it into a cleaned up dataframe
def generate_frame():
    try:
        while True:
            if DEBUG:
                raise RuntimeError
            zip_path = abspath(input("Path of zip file?? : "))
            if isfile(zip_path):
                break
    except:
        # Runtime doesnt support raw inputs
        zip_path = abspath("./data/my_spotify_data.zip")

    filters: list[SongAttributes] = [
        "ts",
        "ms_played",
        "master_metadata_track_name",
        "master_metadata_album_artist_name",
        "master_metadata_album_album_name",
    ]

    compiled_json_path = process_zip(zip_path, filters)
    df = pd.read_json(compiled_json_path)

    # Converting the ts column to datetime object
    df["ts"] = pd.to_datetime(df["ts"])
    return df
