from flask import Flask  , request , url_for

app = Flask(__name__)

@app.route('/childrenBook/')
def index():
    return "hello"



if __name__ == "__main__":
    app.run(debug=True , port=8000 , host="0.0.0.0")