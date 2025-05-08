
from gtts import gTTS
def newVoiceFile(text_voice ,file_name, slow_voice = False):

    language = 'en'

    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=text_voice, lang=language, slow=slow_voice)

    # Saving the converted audio in a mp3 file named
    # welcome 
    file_name = f"{file_name}.mp3"
    myobj.save(f"{file_name}.mp3")
    print(f"voice file saved as {file_name}")
    return file_name


