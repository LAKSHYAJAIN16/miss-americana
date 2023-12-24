import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate(r'C:\Users\USER\Desktop\CS Mr. Penney Stuff\Music Visualizer\server\keys\kronos-3243f-firebase-adminsdk-izkrg-0da3720707.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'kronos-3243f.appspot.com'
})

bucket = storage.bucket()
blob = bucket.blob('test_3.mp3')
outfile=r'C:\Users\USER\Desktop\CS Mr. Penney Stuff\Music Visualizer\data\auds\Infinity.wav'
blob.upload_from_filename(outfile)  
blob.make_public()
print(blob.public_url)