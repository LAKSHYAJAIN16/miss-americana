import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from modules.colours import colour_creator

SAMPLE_DEGREE=2
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
    
    # Get audio analysis, because why not?
    aud_analysis = spotify.audio_analysis(track)
    
    # Establish beat array and get most common beat
    new_beats = []
    for j in aud_analysis["beats"]:
        new_beats.append(round(j["start"], SAMPLE_DEGREE))
         
    # Revise the sections a bit to remove unneccesary data
    new_sections = []
    for k in aud_analysis["sections"]:
        new_sections.append(round(k["start"], SAMPLE_DEGREE))
 
    OUT = {
        "colours" : colors,
        "weight" : weight,
        "type" : type,
        "sections" : new_sections,
        "beats" : new_beats
    }    
    
    # JSON write
    json.dump(OUT, open("data/analysis/" + name + "_by_" + artist + ".json","w+"))
    
    return OUT
