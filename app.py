from flask import Flask  , request , url_for , jsonify , send_file
from qualityEnum import imageQuality
from textMaker import makeTextAI
import childrenStoryMaker as child
import imageAIMaker 
app = Flask(__name__)

staticNumIdPic =0




@app.route('/MagicOfStory/Image',methods=['POST' , 'GET'] )
def create_new_AI_image():
    global staticNumIdPic
    staticNumIdPic+=1
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400  # Handle missing JSON
    
    try:
        inputText = str(data['inputText'])
        ##numImages = int(data['numberOfImages'])
        height  = int(data['height'])
        width  = int(data['width'])
        steps  =imageQuality[str(data['quality'])].value 

        pathImage = imageAIMaker.makeImageAI(inputText , steps , height  , width , staticNumIdPic)
        print("send the file to the user")
        return send_file(pathImage, mimetype='image/png')


    except KeyError:
        return jsonify({"error": "one the values in the JSON is missing"}), 400  # Handle missing JSON
@app.route('/MagicOfStory/ImageAI',methods=['POST'] )    
def create_AI_Image_story_text():
    global staticNumIdPic
    staticNumIdPic+=1
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400  # Handle missing JSON
    
    try:
        textPage = str(data["Text"])
        numPage = int(data["num"])
        #defulte values for the image
        height  = 1080
        width  = 720
        steps  =imageQuality["HIGH"].value 

        #step 1 get a promt to the image generator
        promptPhoto  = makeTextAI("please give me a promt for the AI image generator for this children story text:"+textPage+" try to pay attention to details of the photo , no explaining just send the prompt")
        #step 2 making the photo 
        pathImage = imageAIMaker.makeImageAI(promptPhoto , steps , height  , width , staticNumIdPic)
        #step 3 sending the file 
        print("send the file to the user")
        return send_file(pathImage, mimetype='image/png')





    except KeyError:
        return jsonify({"error": "one the values in the JSON is missing"}), 400  # Handle missing JSON

@app.route('/MagicOfStory/Text',methods=['POST'] )    
def create_new_AI_text():
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400  # Handle missing JSON
    try:
        promt = data.get('input')
        return jsonify({"respond" : makeTextAI(promt)})
    except KeyError:
        return jsonify({"error": "one the values in the JSON is missing"}), 400  # Handle missing JSON

@app.route('/MagicOfStory/Story',methods=['POST'])
def create_new_story():
    global staticNumIdPic
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400  # Handle missing JSON
    try:
        subject = str(data["subject"])
        numPages = int(data["numPages"])
        auther = str(data["auther"])
        description = str(data["description"])
        title = str(data["title"])
        story_obj = child.Story(subject,numPages,auther,description,title ,staticNumIdPic)
        staticNumIdPic+=numPages
        return jsonify(story_obj.to_dict())


    except KeyError:
        return jsonify({"error": "one the values in the JSON is missing"}), 400  # Handle missing JSON
 
if __name__ == "__main__":
    app.run(debug=True , port=5000 , host="0.0.0.0")