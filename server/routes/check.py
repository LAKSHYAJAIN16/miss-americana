import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from modules.main_audio import extract

def check_route(track):
    # Get Track ID
    track_id = track["id"]
    
    # Initialize the Store
    if not firebase_admin._apps:
        cred = credentials.Certificate(r'C:\Users\USER\Desktop\CS Mr. Penney Stuff\Music Visualizer\server\keys\kronos-3243f-firebase-adminsdk-izkrg-0da3720707.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'kronos-3243f.appspot.com'
        })
        
    bucket = storage.bucket()
    blob = bucket.blob('{0}.mp3'.format(track_id))
    if blob.exists():
        # Do nothing
        print("Song {0} by {1} is already indexed".format(track["name"], track["art_string"]))
        return 0
    else:
        try:
            # Download the Mp3 Track
            songPath = extract(track["name"],track["art_string"], track_id)

            # Make Blob
            blob.upload_from_filename(songPath)  
            blob.make_public()
            print("Song {0} by {1} indexed at {2}".format(track["name"], track["art_string"], blob.public_url))
            
            # Delete file after we upload it
            os.remove(songPath)
            return 1
        except:
            # Blacklisted Song
            print("Song {0} by {1} is Blacklisted".format(track["name"], track["art_string"]))
            return 2