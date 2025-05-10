import firebase_admin
from firebase_admin import credentials , storage
from qualityEnum import fileType

def save_file(file_name:str, fileType:fileType):
    cred = credentials.Certificate("private/pawcuts-60a6c-firebase-adminsdk-bnup5-daabf25f72.json")
    firebase_admin.initialize_app(cred,{
        'storageBucket': 'pawcuts-60a6c.appspot.com'
    })


    bucket = storage.bucket()

    # Upload file
    if fileType.value == fileType.mp3:
        blob = bucket.blob(f"voice stories/{file_name}")  # or "images/photo.png"
        blob.upload_from_filename(file_name)
    elif fileType.value == fileType.png:
        blob = bucket.blob(f"Images/{file_name}")  # or "images/photo.png"
        blob.upload_from_filename(file_name)
    # Make file public
    blob.make_public()

    url = blob.public_url
    # Get public URL
    print("Public URL:", url)
    return url

