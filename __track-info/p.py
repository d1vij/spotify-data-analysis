import pandas as pd
import asyncio
from utils.get_track_metadata import *
df = pd.read_json("df.json")

result_df = asyncio.run(get_track_metadata_async(df, concurrency=20))
result_df.to_json("song-genre-data.json")

print(result_df)