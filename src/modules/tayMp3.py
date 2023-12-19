import os
from youtubesearchpython import VideosSearch
from pytube import YouTube

"""
to_mp3 function takes in the name of the song and the name of the artist.
It then uses the VideoSearch API to retrieve results on YouTube.
It then uses pytube to download this as an mp3.
"""
def to_mp3(name, artist):
    # Get the Link of our song
    videosSearch = VideosSearch(name + " by " + artist + " official audio", limit = 1)
    link = videosSearch.result()["result"][0]["link"]
    
    # Download the Mp3
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first() 
    
    # Download to hard drive
    out_file = video.download(r"C:\Users\USER\Desktop\CS Mr. Penney Stuff\Music Visualizer\auds")
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    # Get the path of the file
    path = new_file
    return [path, base]
