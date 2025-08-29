# Fuzzy searching artists / track name
from rapidfuzz import fuzz
import pandas as pd

def get_potential_artists(name: str,_in: pd.DataFrame | pd.Series | list[str], confidence: int, artist_colname="master_metadata_album_artist_name"):

    if(type(_in) == pd.DataFrame):
        artists = _in[artist_colname].values
    elif (type(_in) == pd.Series):
        artists = _in.values
    elif (type(_in) == list[str]):
        artists = _in
    else:
        raise(TypeError(f"Type of {type(_in)} not allowed"))
    
    if(confidence <= 0 or confidence > 100):
        raise ValueError("Confidence must be within 1 to 100")
    
    matched = []
    for artist in artists:
        if(artist is not None):
            if(fuzz.partial_ratio(name.lower(), artist.lower()) >= confidence) and (artist not in matched):
                matched.append(artist)
        
    return matched
    
def get_potential_songs(name: str,_in: pd.DataFrame | pd.Series | list[str], confidence: int, artist_colname="master_metadata_track_name"):

    if(type(_in) == pd.DataFrame):
        songs = _in[artist_colname].values
    elif (type(_in) == pd.Series):
        songs = _in.values
    elif (type(_in) == list[str]):
        songs = _in
    else:
        raise(TypeError(f"Type of {type(_in)} not allowed"))
    
    if(confidence <= 0 or confidence > 100):
        raise ValueError("Confidence must be within 1 to 100")

    matched = []
    for song in songs:
        if(song is not None):
            if(fuzz.token_set_ratio(name.lower(), song.lower()) >= confidence) and (song not in matched):
                matched.append(song)
        
    return matched
    