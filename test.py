apiKey = "AIzaSyCAAhs4cAfwBaHyYfGXkBLi5dhejHOPQtI"

import google.generativeai as genai


genai.configure(api_key=apiKey)

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("""give me a children story about dogs and cats 5 pages""")
print(response.text)
