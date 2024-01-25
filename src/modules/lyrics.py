import requests
import json
import re

def convert_string_to_milliseconds(input_string):
    # Find the index of '[' and ']'
    start_index = input_string.find('[')
    end_index = input_string.find(']')

    # If '[' and ']' are found, proceed to extract and process the time
    if start_index != -1 and end_index != -1:
        time_part = input_string[start_index + 1:end_index]
        remaining_text = input_string[:start_index] + input_string[end_index + 1:]

        # Split the time part into minutes and seconds
        minutes, seconds = map(float, time_part.split(':'))

        # Convert time to milliseconds
        time_in_milliseconds = int((minutes * 60 + seconds) * 1000 * 60)

        return time_in_milliseconds, remaining_text.strip()

    # If '[' and ']' are not found, return default values
    return 0, input_string.strip()


"""
The Lyrics Thread uses an open source lyric api to scrape synced lyrics
"""
def lyricThread(name, artist):
    # Assemble URL
    url = "https://lrclib.net/api/search?track_name={0}&artist_name={1}"
    url = url.format(name, artist)

    # Send Web request
    lyrics = requests.get(url).json()

    # Retrieve actual text of lyrics
    print(lyrics[0])
    our_lyrics = lyrics[0]["syncedLyrics"].split("\n")

    # Store it on local computer
    json.dump(our_lyrics, open("data/lyrics/" + name + "_by_" + artist + ".json","w+"))

    # Format array
    l = []
    for m in our_lyrics:
        time, lyric = convert_string_to_milliseconds(m)
        l.append([time, lyric])

    return l