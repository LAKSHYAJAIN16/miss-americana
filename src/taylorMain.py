import os
import time
import spotipy
import threading
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
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

# Actual Audio Visual Processing
def aud_vis(wavFile, mqtt : mqtt.Client):
    mqtt.loop_start()
    mqtt.loop_stop()
    # Retrieve the data from the wav file
    data, samplerate = sf.read(wavFile)

    n = len(data)  # the length of the arrays contained in data
    Fs = samplerate  # the sample rate
    print((1 / Fs)*1000)
    
    # Working with stereo audio, there are two channels in the audio data.
    # Let's retrieve each channel seperately:
    ch1 = np.array([data[i][0] for i in range(n)])  # channel 1
    ch2 = np.array([data[i][1] for i in range(n)])  # channel 2

    # x-axis and y-axis to plot the audio data
    time_axis = np.linspace(0, n / Fs, n, endpoint=False)
    sound_axis = ch1

    def playing_audio():
        song = AudioSegment.from_wav(wavFile)
        play(song)

    def showing_audiotrack():
        # We use a variable previousTime to store the time when a plot update is made
        # and to then compute the time taken to update the plot of the audio data.
        previousTime = time.time()

        # Turning the interactive mode on
        plt.ion()

        # Each time we go through a number of samples in the audio data that corresponds to one second of audio,
        # we increase spentTime by one (1 second).
        spentTime = 0

        # Let's the define the update periodicity
        updatePeriodicity = 5 # expressed in seconds

        # Plotting the audio data and updating the plot
        for i in range(n):
            # Each time we read one second of audio data, we increase spentTime :
            if i // Fs != (i-1) // Fs:
                spentTime += 1

            # We update the plot every updatePeriodicity seconds
            if spentTime == updatePeriodicity:
                # Clear the previous plot
                plt.clf()

                # Plot the audio data
                plt.plot(time_axis, sound_axis)

                # Plot a red line to keep track of the progression
                plt.axvline(x=i / Fs, color='r')
                plt.xlabel("Time (s)")
                plt.ylabel("Audio")
                plt.show()  # shows the plot
                plt.pause(updatePeriodicity-(time.time()-previousTime))

                # a forced pause to synchronize the audio being played with the audio track being displayed
                previousTime = time.time()
                spentTime = 0

    p1 = Process(target=playing_audio, args=())
    p1.start()
    p2 = Process(target=showing_audiotrack, args=())
    p2.start()
    p1.join()
    p2.join()
    
n = input("Enter the name of the Song: ")
artist = input("Enter the name of the Artist : ")

# MQTT STUFF
client = mqtt.Client()
client.username_pw_set("gkvpckep", "yGbZQKc8MAma")
client.connect("awesome-fisher.cloudmqtt.com", 1883, 60)
client.loop_start()

def youTubeThread(name, artist, client):
    mp3 = to_mp3(name, artist)
    wav = to_wav(mp3)

    # Now, we Pass it to the audVis module
    aud_vis(wav, client)
    
def spotifyThread(name, artist, client):  
    # Init Spotify
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="7f9b0d52c40944878346f258892e14d3", client_secret="93fcf0381dec406c8c9bc55c07b739e2"))
    
    # Get TrackID
    results = spotify.search(name + " by " + artist, 1, type="track")
    track = results["tracks"]["items"][0]["id"]
    print(track)
    
    # Retrieve Audio Features (standard)
    standardAudioFeats = spotify.audio_features([track])[0]
    dance = standardAudioFeats["danceability"]
    energy = standardAudioFeats["energy"]
    tempo = standardAudioFeats["tempo"]
    valence = standardAudioFeats["valence"]
    
    # Do some algorithm processing $#!7 to get the colours, because why not?
    colors, weight = colour_creator(dance, energy, tempo, valence)
    
# Run both threads concurrently
t1 = threading.Thread(target=youTubeThread, args=(n, artist, client))
t2 = threading.Thread(target=spotifyThread, args=(n, artist, client))
# t1.start()
t2.start()
# t1.join()
t2.join()

print("Program Suspended")
client.loop_stop()