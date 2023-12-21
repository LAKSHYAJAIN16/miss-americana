import json
import spotipy
import time
import sched
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
BUFFER_SIZE_SECTIONS = 5
BUFFER_SIZE_BEATS = 30
BUFFER_SIZE_SEGMENTS = 70
SAMPLE_DEGREE = 2
SAMPLE_RATE = 10^(-SAMPLE_DEGREE)

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
        new_beats[-1].append(round(j["start"], SAMPLE_DEGREE))
        new_beats[-1].append(round(j["duration"], SAMPLE_DEGREE))
        
    new_sections = []
    for k in aud_analysis["sections"]:
        new_sections.append([])
        new_sections[-1].append(round(k["start"], SAMPLE_DEGREE))
        new_sections[-1].append(round(k["loudness"], SAMPLE_DEGREE))
        
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
    return [song, wav]

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
print(spotify["colours"])
for k in range(len(spotify["colours"])):
    client.publish("RICKASTLEY","3:{0}:{1}".format(k, spotify["colours"][k]))

# Then, we send the first load of sections (first send initialization message and then the content)
client.publish("RICKASTLEY","4:S:none")
cur_sections_iter = 0
sectionBuf = spotify["sections"][cur_sections_iter:cur_sections_iter + BUFFER_SIZE_SECTIONS]
print(sectionBuf)
for m in range(len(sectionBuf)):
    client.publish("RICKASTLEY","4:N:{0}:{1}".format(m, sectionBuf[m][0]))
    client.publish("RICKASTLEY","4:M:{0}:{1}".format(m, sectionBuf[m][1]))

# Get length of song
sf_file = sf.SoundFile(song[1])
dur = round((sf_file.frames / sf_file.samplerate),2)
play(song[0])

# Send the data
client.loop_stop()