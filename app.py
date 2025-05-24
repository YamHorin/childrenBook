from flask import Flask  , request , url_for , jsonify , send_file
from qualityEnum import imageQuality 
from textMaker import makeTextAI
import childrenStoryMaker as child
import imageAIMaker 
import voiceMaker
from memoryManager import initialize_app
import exceptionHandler as ex
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)

staticNumIdPic =0


@app.route('/MagicOfStory/test',methods=['POST' , 'GET'] )
def test():
    return "hello world"


@app.route('/MagicOfStory/ImageFromImage',methods=['POST'] )
def create_new_AI_image_from_image():
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return ex.exception_no_json()
    
    try:
        textPage = str(data["Text"])
        url_image = str(data["url_image"])
        pathImage = imageAIMaker.makeImageFromImage(textPage , url_image)
        print(f"send the file to the user")
        return jsonify({"link":pathImage}), 200  # Handle missing JSON

    except KeyError as e:
        return ex.exception_json_value(e)
    except ResourceExhausted as e:
        return ex.exception_ResourceExhausted(e)
    except Exception as e:
        return ex.exception_internal_server_issue(e)

@app.route('/MagicOfStory/ImageAI',methods=['POST'] )    
def create_AI_Image_story_text():
    global staticNumIdPic
    staticNumIdPic+=1
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return ex.exception_no_json()
    
    try:
        textPage = str(data["Text"])
        promptPhoto  = makeTextAI("please give me a promt for the AI image generator for this children story text:"+textPage+" try to pay attention to details of the photo")
        pathImage = imageAIMaker.makeImageAI(promptPhoto)
        print("send the file to the user")
        return jsonify({"link":pathImage}), 200  # Handle missing JSON

    except KeyError as e:
        return ex.exception_json_value(e)
    except ResourceExhausted as e:
        return ex.exception_ResourceExhausted(e)
    except Exception as e:
        return ex.exception_internal_server_issue(e)
@app.route('/MagicOfStory/Text',methods=['POST'] )    
def create_new_AI_text():
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return ex.exception_no_json()
    try:
        promt = data.get('input')
        return jsonify({"respond" : makeTextAI(promt)})
    except KeyError as e:
        return ex.exception_json_value(e)
    except ResourceExhausted as e:
        return ex.exception_ResourceExhausted(e)
    except Exception as e:
        return ex.exception_internal_server_issue(e)

@app.route('/MagicOfStory/Story',methods=['POST'])
def create_new_story():
    global staticNumIdPic
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return ex.exception_no_json()
    try:
        subject = str(data["subject"])
        numPages = int(data["numPages"])
        auther = str(data["auther"])
        description = str(data["description"])
        title = str(data["title"])
        enable_voice = bool(data["text_to_voice"])
        #optional value , don't raise exception
        pages_texts_list = list(data.get("story_pages",[]))
        story_obj = child.Story(subject , numPages, auther , description,title, pages_texts_list , enable_voice)
        return jsonify(story_obj.to_dict())

    except KeyError as e:
        return ex.exception_json_value(e)
    except ResourceExhausted as e:
        return ex.exception_ResourceExhausted(e)
    except Exception as e:
        return ex.exception_internal_server_issue(e)
    


@app.route('/MagicOfStory/Story/Sequel',methods=['POST'])
def create_new_story_sequel():
    global staticNumIdPic
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return ex.exception_no_json()
    try:
        numPages = int(data["numPages"])
        auther = str(data["auther"])
        description = str(data["description"])
        title = str(data["title"])
        enable_voice = bool(data["text_to_voice"])
        pages_previous = list(data["pages_previous"])
        title_previous = str(data["title_previous"])

        story_obj = child.Continued_story(numPages,auther,description,title ,staticNumIdPic,pages_previous,title_previous ,make_voice=enable_voice)
        staticNumIdPic+=numPages
        return jsonify(story_obj.to_dict())


    except KeyError as e:
        return ex.exception_json_value(e)
    except ResourceExhausted as e:
        return ex.exception_ResourceExhausted(e)
    except Exception as e:
        return ex.exception_internal_server_issue(e)
@app.route('/MagicOfStory/voice',methods=['POST']) 
def make_new_text_to_speach():
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        ex.exception_no_json()
    try:
        text = str(data["text_page"])
        story = str(data["story_title"])
        url_file  = voiceMaker.newVoiceFile(text , f"{story}.mp3")
        return jsonify({"url": url_file})

    except KeyError as e:
        return ex.exception_json_value(e)
    except ResourceExhausted as e:
        return ex.exception_ResourceExhausted(e)
    except Exception as e:
        return ex.exception_internal_server_issue(e)

if __name__ == "__main__":
    initialize_app()
    app.run(debug=True , port=5000 , host="0.0.0.0")