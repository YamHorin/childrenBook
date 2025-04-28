import os
import google.generativeai as genai
from dotenv import load_dotenv


def makeTextAI(promt):
    load_dotenv(override= True)
    apiKey = os.getenv("API_KEY")
    genai.configure(api_key=apiKey)

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(promt)
    return response.text
        
#test

subject = "dogs and cats"
numPages = 3
message = f'''
You are currently a children's writer who is required to write a children's book about {subject}
You are required to write {numPages} pages with each page no more than 100 words
Return the respond as follow:
Page 1: Text of page 1
Page 2: Text of page 2
And so on

'''
print(makeTextAI(message))