import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
def create_client():
    load_dotenv()
    auth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-currently-playing user-read-playback-state user-modify-playback-state",
        cache_path=".spotify_cache"
            
    ) 
    return spotipy.Spotify(auth_manager=auth)

def get_current_track(sp):
    result = sp.current_playback()
    if result is None or not result.get("is_playing"):
            return None
    item = result["item"]
    return {
        "id":       item["id"],
        "title":    item["name"],
        "artist":   item["artists"][0]["name"],
        "album":    item["album"]["name"],
        "duration": item["duration_ms"],
        "progress": result["progress_ms"],
    }


def play_pause(sp):
    state = sp.current_playback()
    if state and state["is_playing"]:
        sp.pause_playback()
    else:
        sp.start_playback()

def next_track(sp):
    sp.next_track()

def prev_track(sp):
    sp.previous_track()

