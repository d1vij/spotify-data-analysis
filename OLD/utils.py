from dotenv import load_dotenv
from os import path, remove, getenv
from json import dumps
from spotipy import Spotify, SpotifyOAuth

env_path = '.env'

def getApi() -> Spotify:
    """ wrapper to generate spotipy api object
        https://spotipy.readthedocs.io/en/2.25.1
        https://developer.spotify.com/documentation/web-api
    """
    try :
        # clearing existing cache file
        if path.exists('.cache'): remove('.cache')

        load_dotenv(dotenv_path=env_path, override=True) # override ensures that no cached scope is present 
        scopes = getenv("SPOTIPY_SCOPES")
        print("Loaded SCOPES:", scopes)
        return  Spotify(auth_manager=SpotifyOAuth(
                        client_id=getenv("CLIENT_ID"),
                        client_secret=getenv("CLIENT_SECRET"),
                        scope=getenv("SPOTIPY_SCOPES"),
                        redirect_uri=getenv("SPOTIPY_REDIRECT_URI")
                    ))
    except Exception as e:
        print(e)

            
def print_json(obj : dict|None):
    print(dumps(obj, indent=2))