import requests
import json

def lyricThread(name, artist):
    # Assemble URL
    url = "https://lrclib.net/api/search?track_name={0}&artist_name={1}"
    url = url.format(name, artist)
    lyrics = requests.get(url).json()
    our_lyrics = lyrics[0]["syncedLyrics"].split("\n")
    json.dump(our_lyrics, open("lyrics/" + n + "_by_" + artist + ".json","w+"))
    return our_lyrics