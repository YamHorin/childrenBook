# AI server for final project "קסם של סיפור"
## how to run 
1. clone this repo 
 ```bash
git clone https://github.com/YamHorin/childrenBook.git
```

2. run pip install to install all the libraries needed
 ```bash
pip install -r requirements.txt
```
3. recommended to make virtual environment to run the code from here , to activate the evironment:
 ```bash
cd .venv
cd scripts
./activate
cd ..
```
4. run app.py file 
 ```bash
python app.py
```

## docker
* you can run the enviroment with docker 
* to install the docker use the docker file 


## jsons for the server:
```json
json photo: 
{
    "inputText" :"a boy goes to school , cartoon style ",

}

json story media (function1)

{
"subject":"cats and dogs",
"numPages":"3",
"auther":"Yam Horin",
"description":"a cute story about how dogs and cats can become friends",
"title":"cats and dogs",
"text_to_voice":true,
"story_pages" : [
    "Once upon a time, in a quiet forest, there lived a curious fox named Felix.",
    "Felix loved to explore the woods and discover new things every day.",
    "One morning, he stumbled upon a shiny key hidden beneath a pile of leaves."
]


}



json story AI (function2): 
{

"subject":"cats and dogs",
"numPages":"3",
"auther":"Yam Horin",
"description":"a cute story about how dogs and cats can become friends",
"title":"cats and dogs",
"text_to_voice":true
}




json sequel story (function3):


{

"subject":"cats and dogs2",
"numPages":"3",
"auther":"Yam Horin",
"description":"a cute story about how dogs and cats can become friends",
"title":"cats and dogs",
"text_to_voice":true,
"pages_previous": [
        {
            "img_url": "image 0.png",
            "text_page": "Whiskers twitched!  A fluffy cat, Mittens, saw a bouncy dog, Buster.  They stared.  Would they play?",
            "voice_file_url": null
        },
        {
            "img_url": "image 1.png",
            "text_page": "Buster wagged his tail, a happy thump! Mittens slowly blinked.  A tiny meow escaped.  Friends?",
            "voice_file_url": null
        },
        {
            "img_url": "image 2.png",
            "text_page": "They chased a bright red ball,  laughing and barking and purring.  A new friendship bloomed!",
            "voice_file_url": null
        }
    ],
"title_previous":"cats and dogs"

}

json option story return example 

{
    "auther": "Yam Horin",
    "description": "a cute story about how dogs and cats can become friends",
    "numPages": 6,
    "pages": [
        {
            "img_url": "https://storage.googleapis.com/pawcuts-60a6c.appspot.com/Images/image%20c9d3c.png",
            "text_page": "Once upon a time, in a quiet forest, there lived a curious fox named Felix.",
            "voice_file_url": null
        },
        {
            "img_url": "https://storage.googleapis.com/pawcuts-60a6c.appspot.com/Images/image%2037798.png",
            "text_page": "Felix loved to explore the woods and discover new things every day.",
            "voice_file_url": null
        },
        {
            "img_url": "https://storage.googleapis.com/pawcuts-60a6c.appspot.com/Images/image%208ff8b.png",
            "text_page": "One morning, he stumbled upon a shiny key hidden beneath a pile of leaves.",
            "voice_file_url": null
        },
        {
            "img_url": "https://storage.googleapis.com/pawcuts-60a6c.appspot.com/Images/image%2026c1d.png",
            "text_page": "Excited, Felix wondered what the key could unlock, and he set off on a quest to find out.",
            "voice_file_url": null
        },
        {
            "img_url": "https://storage.googleapis.com/pawcuts-60a6c.appspot.com/Images/image%20c92f1.png",
            "text_page": "He asked the wise old owl, who told him of a hidden treasure deep in the forest.",
            "voice_file_url": null
        },
        {
            "img_url": "https://storage.googleapis.com/pawcuts-60a6c.appspot.com/Images/image%20a1694.png",
            "text_page": "Felix followed clues carved into trees and hidden under rocks.",
            "voice_file_url": null
        }
    ],
    "title": "cats and dogs"
}


```
