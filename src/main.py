import json
import spotipy
import time
import sched
import requests
import paho.mqtt.client as mqtt

from pydub import AudioSegment
from pydub.playback import play
from spotipy.oauth2 import SpotifyClientCredentials

from modules.spotify import spotifyThread
from modules.youtube import youtubeThread
from modules.lyrics import lyricThread
from utils.taylorThreading import ThreadWithReturnValue

# Some config variables
BUFFER_SIZE_SECTIONS = 5
BUFFER_SIZE_BEATS = 30
BUFFER_SIZE_SEGMENTS = 70
SAMPLE_DEGREE = 2
SAMPLE_RATE = 10^(-SAMPLE_DEGREE)

# Enter name of song and artist 
n = input("Enter the name of the Song: ")
artist = input("Enter the name of the Artist : ")

# MQTT STUFF
client = mqtt.Client()
client.username_pw_set("gkvpckep", "yGbZQKc8MAma")
client.connect("awesome-fisher.cloudmqtt.com", 1883, 60)
client.loop_start()

def mqtt_initialization(spotify, lyrics, song, client):
    # Start communication for MQTT. This is sort of a 'header' message.
    client.publish("RICKASTLEY", "START_PROCESSING")

    # First, send the name and artist
    client.publish("RICKASTLEY","1:{0}".format(n))
    client.publish("RICKASTLEY","2:{0}".format(artist))

    # Print the Colours
    print(spotify["colours"])

    # Send them one by one ot the arduino
    for k in range(len(spotify["colours"])):
        client.publish("RICKASTLEY","3:{0}:{1}".format(k, spotify["colours"][k]))

    # Then, we send the initialization message to start our sections
    client.publish("RICKASTLEY","4:S:none")

    # Iterator to keep track of the index we need to send it to in the arduino arrah
    cur_sections_iter = 0

    # Format the array so that we get a new 30 elements
    sectionBuf = spotify["sections"][0:BUFFER_SIZE_SECTIONS]

    # Print the sections
    print(sectionBuf)

    # Send the sections. Eachs section is sent 
    for m in range(len(sectionBuf)):
        client.publish("RICKASTLEY","4:N:{0}:{1}".format(m, sectionBuf[m][0]))
        client.publish("RICKASTLEY","4:M:{0}:{1}".format(m, sectionBuf[m][1])) 

# Threads, because WTF IS GOING ON
t1 = ThreadWithReturnValue(target=spotifyThread, args=(n, artist))
t2 = ThreadWithReturnValue(target=youtubeThread, args=(n, artist))
t3 = ThreadWithReturnValue(target=lyricThread, args=(n, artist))

# Start threads
t3.start()
t2.start()
t1.start()
lyrics = t3.join()
spotify = t1.join()
song = t2.join()

# Initialize MQTT
mqtt_initialization(spotify, lyrics, song, client)

# Get length of song 
sf_file = sf.SoundFile(song[1])
dur = round((sf_file.frames / sf_file.samplerate),2)

# Play song
play(song[0])

# Stop program
client.loop_stop()
print("EXITING")