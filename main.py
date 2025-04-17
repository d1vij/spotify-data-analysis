#TODO: work on postgres connectivity

"""
-> simple script to parse spotify's "Extended Streaming History" and store it into db



-> instead of using datetime functions,
 sqllite3 uses python datetime's strftime with formatting string
 for eg, to extract the year from current date-time format use => strftime('%Y','2024-03-14 23:09:33') -> '2024'
 comparision can be done through this extraction
 %Y -> year YYYY
 %m -> month mm
 %d -> day dd
 %H -> hour 24 HH
 %M -> minute MM
 %S -> seconds SS
 %I -> am/pm timestamp
"""










import json
import sqlite3
from datetime import datetime
from os import listdir
import os
#parsing json

USE_EXTERNAL_DB = False #NOTE:WORK upon this
FOLDER_PATH = '.' #path which has the json files

connection_string = "postgresql://postgres:1234@localhost:5432/spotifyparsertest"



#helper functions
def load_filenames() -> list[str] :
    return [filepath for filepath in listdir(FOLDER_PATH) if (filepath.startswith("Streaming_History_Audio_") and filepath.endswith(".json"))]

def normalize(string : str) -> str:
    return string.lower().strip() if type(string) == str else string

def iso8601_to_dt(string : str) -> str:
    #converts the iso8601 time standard datetime string provided by spotify
    #to simplified datetime string for database
    #eg '2020-11-27t07:19:29z' -> '2020-11-27 07:19:29'

    dt_obj = datetime.fromisoformat(string.replace('Z','+00:00')) #Z implies utc +0 timezone
    return datetime.strftime(dt_obj, "%Y-%m-%d %H:%M:%S")
    

parsed_data : list[tuple] = []

files = load_filenames()
print(files)

for name in files:
    with open(name, encoding='utf-8',mode='r') as file:
        raw_data = file.read()
    data : list[dict] = json.loads(raw_data)
    entry : dict = None
    for entry  in data:
        parsed_data.append((
                                        iso8601_to_dt(entry.get("ts")),
                                        normalize(entry.get("platform")),
                                        normalize(entry.get("ms_played")),
                                        normalize(entry.get("master_metadata_track_name")),
                                        normalize(entry.get("master_metadata_album_artist_name")),
                                        normalize(entry.get("master_metadata_album_album_name")),
                                        normalize(entry.get(""))
                                        
                                        )
                           )
    print(len(parsed_data))
    


    
#database initialization
conn = sqlite3.connect("anant.db")
cursor = conn.cursor()

cursor.execute("drop table if exists spotify")
conn.commit()

cursor.execute("""create table if not exists spotify(
                    timestamp datetime,
                    platform varchar(255),
                    ms_played int,
                    track_name varchar(255),
                    artist_name varchar(255),
                    album_name varchar(255),
                    track_url varchar(255) defautl null
                ); """)
conn.commit()

#data entry
print(list(parsed_data[0]))



cursor.executemany("insert into spotify(timestamp, platform, ms_played, track_name, artist_name, album_name) values(?,?,?,?,?,?)", parsed_data)
conn.commit()

print("Succesfullly inserted ", len(parsed_data), " rows")
cursor.close()
conn.close()