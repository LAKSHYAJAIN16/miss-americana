import json
import spotipy
import threading
import requests
import soundfile as sf
import paho.mqtt.client as mqtt

from pydub import AudioSegment
from pydub.playback import play
from spotipy.oauth2 import SpotifyClientCredentials

from modules.taylorColours import colour_creator
from modules.tayMp3 import to_mp3
from modules.tayWav import to_wav
from utils.taylorThreading import ThreadWithReturnValue

# Enter name of song and artist 
n = input("Enter the name of the Song: ")
artist = input("Enter the name of the Artist : ")

# MQTT STUFF
client = mqtt.Client()
client.username_pw_set("gkvpckep", "yGbZQKc8MAma")
client.connect("awesome-fisher.cloudmqtt.com", 1883, 60)
client.loop_start()
  
def spotifyThread(name, artist):  
    # Init Spotify
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="7f9b0d52c40944878346f258892e14d3", client_secret="93fcf0381dec406c8c9bc55c07b739e2"))
    
    # Get TrackID
    results = spotify.search(name + " by " + artist, 1, type="track")
    track = results["tracks"]["items"][0]["id"]
    print(track)
    
    # Retrieve Audio Features (standard)
    standardAudioFeats = spotify.audio_features([track])[0]
    acoustic = standardAudioFeats["acousticness"]
    dance = standardAudioFeats["danceability"]
    energy = standardAudioFeats["energy"]
    tempo = standardAudioFeats["tempo"]
    valence = standardAudioFeats["valence"]
    
    # Do some algorithm processing $#!7 to get the colours, because why not?
    colors, weight, type = colour_creator(acoustic, dance, energy, tempo, valence)
    print(colors)
    print(weight)
    print(type)
    
    # Get audio analysis, because why not?
    aud_analysis = spotify.audio_analysis(track)
    
    # Revise the sections a bit to remove unneccesary data
    new_beats = []
    for j in aud_analysis["beats"]:
        new_beats.append([])
        new_beats[-1].append(round(j["start"], 2))
        new_beats[-1].append(round(j["duration"], 2))
        
    new_sections = []
    for k in aud_analysis["sections"]:
        new_sections.append(k["start"])
        
    OUT = {
        "track_id" : track,
        "colours" : colors,
        "weight" : weight,
        "type" : type,
        "sections" : new_sections,
        "beats" : new_beats
    }    
    
    # JSON write
    json.dump(OUT, open("analysis/" + n + "_by_" + artist + ".json","w+"))
    
    return OUT

def youtubeThread(name, artist):
    # YouTube Thread
    mp3 = to_mp3(name, artist)
    wav = to_wav(mp3)

    # Retrieve the data from the wav file
    data, samplerate = sf.read(wav)

    n = len(data)  # the length of the arrays contained in data
    Fs = samplerate  # the sample rate
    print((1 / Fs)*1000)
    
    # Play Song
    song = AudioSegment.from_wav(wav)
    return song

def lyricThread(name, artist):
    # Assemble URL
    url = "https://lrclib.net/api/search?track_name={0}&artist_name={1}"
    url = url.format(name, artist)
    lyrics = requests.get(url).json()
    our_lyrics = lyrics[0]["syncedLyrics"].split("\n")
    json.dump(our_lyrics, open("lyrics/" + n + "_by_" + artist + ".json","w+"))
    return our_lyrics
    
# Threads, because WTF IS GOING ON
t1 = ThreadWithReturnValue(target=spotifyThread, args=(n, artist))
t2 = ThreadWithReturnValue(target=youtubeThread, args=(n, artist))
t3 = ThreadWithReturnValue(target=lyricThread, args=(n, artist))

# Spotify Thread
t3.start()
t2.start()
t1.start()
lyrics = t3.join()
spotify = t1.join()
song = t2.join()

# Start communication for MQTT
client.publish("RICKASTLEY", "START_PROCESSING")

# First, send the name and artist
client.publish("RICKASTLEY","1:{0}".format(n))
client.publish("RICKASTLEY","2:{0}".format(artist))

# Then we send the colors
for k in range(len(spotify["colours"])):
    client.publish("RICKASTLEY","3:{k}:{0}".format(spotify["colours"][k]))

# Send the data
client.loop_stop()