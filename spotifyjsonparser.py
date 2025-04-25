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
from os import listdir, path

#helper functions
def normalize(string : str) -> str:
    return string.lower().strip() if type(string) == str else string

def iso8601_to_dt(string : str) -> str:
    #converts the iso8601 time standard datetime string provided by spotify
    #to simplified datetime string for database
    #eg '2020-11-27t07:19:29z' -> '2020-11-27 07:19:29'

    dt_obj = datetime.fromisoformat(string.replace('Z','+00:00')) #Z implies utc +0 timezone
    return datetime.strftime(dt_obj, "%Y-%m-%d %H:%M:%S")

def parse_and_load(folder_path='.', database_name='database' ,use_external_database : bool =False) -> None:
    """
    :param folder_path: folder having spotify json data
    :param database_name: name of local sqlite database
    :param use_external_database: use external database, database name becomes irrelevant here
    :return: None
    """

    parsed_data : list[tuple] = []

    files = [path.join(folder_path,filepath) for filepath in listdir(folder_path) if (filepath.startswith("Streaming_History_Audio_") and filepath.endswith(".json"))]
    print("Found files ",len(files), files)

    for name in files:
        try:
            with open(name, encoding='utf-8',mode='r') as file:
                raw_data : str = file.read()
        except Exception as e:
            print(e)
            continue


        data : list[dict] = json.loads(raw_data)
        entry : dict = {}
        for entry in data:
            # each row is a track entry
            parsed_data.append((
                iso8601_to_dt(entry.get("ts")),
                normalize(entry.get("ms_played")),
                normalize(entry.get("master_metadata_track_name")),
                normalize(entry.get("master_metadata_album_artist_name")),
                normalize(entry.get("master_metadata_album_album_name")),
                entry.get("spotify_track_uri")
                ))

    print("Total tracks queried : ", len(parsed_data))

    #database initialization
    conn = sqlite3.connect(database_name+'.db')
    cursor = conn.cursor()

    cursor.execute("drop table if exists spotify")
    conn.commit()

    cursor.execute("""create table if not exists spotify(
                        timestamp datetime,
                        ms_played int,
                        track_name varchar(255),
                        artist_name varchar(255),
                        album_name varchar(255),
                        track_uri varchar(255) default null,
                        artist_uri varchar(255) default null,
                        track_genre text default null,
                        track_popularity int default 0
                    ); """)
    conn.commit()

    #data entry
    entry : tuple = ()
    count = 0
    for entry in parsed_data:
        try:
            cursor.execute("insert into spotify(timestamp, ms_played, track_name, artist_name, album_name,track_uri,artist_uri, track_genre, track_popularity) values(?,?,?,?,?,?,?,?,?)", entry+(None,None, 0))
            count += 1
        except Exception as e:
            print("cutie", e)

    conn.commit()

    cursor.close()
    conn.close()

    print(f"Successfully inserted {count} items, {len(parsed_data) - count} yielded error")


