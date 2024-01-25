import paho.mqtt.client as mqtt
import time

from pydub import AudioSegment
from pydub.playback import play
from spotipy.oauth2 import SpotifyClientCredentials

from modules.spotify import spotifyThread
from modules.youtube import youtubeThread
from modules.lyrics import lyricThread
from utils.taylorThreading import ThreadWithReturnValue

# Enter name of song and artist 
n = input("Enter the name of the Song: ")
artist = input("Enter the name of the Artist : ")

# MQTT Initialization
client = mqtt.Client()
client.username_pw_set("gkvpckep", "yGbZQKc8MAma")
client.connect("awesome-fisher.cloudmqtt.com", 1883, 60)
client.loop_start()

# MQTT function
def mqtt_initialization(spotify, lyrics, client):
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

    # Send the sections. Eachs section is sent 
    sectionBuf = spotify["sections"]
    for m in range(len(sectionBuf)):
        client.publish("RICKASTLEY","4:{0}".format(sectionBuf[m]))
        
    # Format the beats array so we get a new Beats_Buffer amount
    beats_buf = spotify["beats"]
    for l in range(len(beats_buf)):
        client.publish("RICKASTLEY","5:{0}".format(beats_buf[m]))

    # Send the Lyrics
    for l in range(len(lyrics)):
        client.publish("RICKASTLEY","6:{0}".format(lyrics[l][0]))
        client.publish("RICKASTLEY","7:{0}".format(lyrics[l][1]))

    # Stop Communicating
    client.publish("RICKASTLEY","STOP")

# Run all of the requests concurrently, to optimize program
t1 = ThreadWithReturnValue(target=spotifyThread, args=(n, artist))
t2 = ThreadWithReturnValue(target=youtubeThread, args=(n, artist))
t3 = ThreadWithReturnValue(target=lyricThread, args=(n, artist))

# Start threads
t3.start()
t2.start()
t1.start()

# Wait for threads to end
lyrics = t3.join()
spotify = t1.join()
song = t2.join()

# Initialize MQTT
mqtt_initialization(spotify, lyrics, client)

# Wait a little bit to account for the delay
time.sleep(2)

# Play song
play(song[0])

# Stop program
client.loop_stop()
print("EXITING")