import os
import json
import spotipy
import threading
import subprocess
import requests
import paho.mqtt.client as mqtt

from youtubesearchpython import VideosSearch
from pytube import YouTube
from multiprocessing import Process
from pydub import AudioSegment
from pydub.playback import play
from spotipy.oauth2 import SpotifyClientCredentials

from taylorColours import colour_creator

# Converts Name and Artist to mp3 using the YouTube API
def to_mp3(name, artist):
    # Get the Link of our song
    videosSearch = VideosSearch(name + " by " + artist + " official audio", limit = 1)
    link = videosSearch.result()["result"][0]["link"]
    
    # Download the Mp3
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first() 
    out_file = video.download(r"C:\Users\USER\Desktop\CS Mr. Penney Stuff\Music Visualizer\auds")
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    # Get the path of the file
    path = new_file
    return [path, base]

# Converts mp3 file to wav using ffmpeg
def to_wav(mp3):
    subprocess.call(['ffmpeg','-i',mp3[0],mp3[1]+".wav"])
    return mp3[1]+".wav"

# Enter name of song and artist 
n = input("Enter the name of the Song: ")
artist = input("Enter the name of the Artist : ")

# MQTT STUFF
client = mqtt.Client()
client.username_pw_set("gkvpckep", "yGbZQKc8MAma")
client.connect("awesome-fisher.cloudmqtt.com", 1883, 60)
client.loop_start()
  
def spotifyThread(name, artist, client):  
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
    
    # Output the analysis to our folder, because why not?
    json.dump(aud_analysis, open("analysis/" + n + "_by_" + artist + ".json","w+"))

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
    play(song)

def lyricThread(name, artist):
    # Assemble URL
    url = "https://lrclib.net/api/search?track_name={0}&artist_name={1}"
    url = url.format(name, artist)
    lyrics = requests.get(url).json()
    our_lyrics = lyrics[0]["syncedLyrics"].split("\n")
    json.dump(our_lyrics, open("lyrics/" + n + "_by_" + artist + ".json","w+"))
    
# Threads, because WTF IS GOING ON
t1 = threading.Thread(target=spotifyThread, args=(n, artist, client))
t2 = threading.Thread(target=youtubeThread, args=(n, artist))
t3 = threading.Thread(target=lyricThread, args=(n, artist))

# Spotify Thread
t3.start()
# t1.start()
t3.join()
# t1.join()
# t2.start()
# t2.join()
client.loop_stop()