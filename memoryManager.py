import firebase_admin
from firebase_admin import credentials , storage
from qualityEnum import fileType

def initialize_app():
    cred = credentials.Certificate("private/pawcuts-60a6c-firebase-adminsdk-bnup5-daabf25f72.json")
    firebase_admin.initialize_app(cred,{
        'storageBucket': 'pawcuts-60a6c.appspot.com'
    })
    

def save_file(file_name:str, fileType:fileType):
    


    bucket = storage.bucket()
    url = ''
    # Upload file
    if fileType.value == fileType.mp3.value:
        blob = bucket.blob(f"voice stories/{file_name}")  # or "images/photo.png"
        blob.upload_from_filename(file_name)
        blob.make_public()
        url = blob.public_url
    elif fileType.value == fileType.png.value:
        blob = bucket.blob(f"Images/{file_name}")  # or "images/photo.png"
        blob.upload_from_filename(file_name)
        blob.make_public()
        url = blob.public_url

    print("Public URL:", url)
    return url

