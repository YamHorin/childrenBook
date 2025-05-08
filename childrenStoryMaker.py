import textMaker as t
from voiceMaker import newVoiceFile
import imageAIMaker 
import re
from qualityEnum import imageQuality
from random import randint 

def storyTextSplit(text):
    matches = re.split(r'Page \d+:\s', text)
    # Remove the first empty string if it exists, and strip whitespace
    arr = [page.strip() for page in matches if page.strip()]
    print(arr)
    return arr

class page():
    def __init__(self , text_page, img_url , voice_file_url):
        self.text_page = text_page
        self.img_url = img_url
        self.voice_file_url = voice_file_url
    
    def get_text_page(self):
        return self._text_page

    def set_text_page(self, text_page):
        self._text_page = text_page

    def get_img_url(self):
        return self._img_url

    def set_img_url(self, img_url):
        self._img_url = img_url

    def to_dict(self):
        return {
            'text_page': self.text_page,
            'img_url': self.img_url,
            'voice_file_url':self.voice_file_url
        }

    


class Story():
    def __init__(self , subject , numPages , auther , description , title ,
                  staticNumIdPic,height_images = 1080 , width_images = 1080 , 
                  quality_images = 'MEDIUM',make_voice = True):
        
        self.numPages = numPages
        self.description = description
        self.auther =auther
        story = ''
        extra_promt = " , just print the answer"
        self.pages = []
        if title!= '':
            self.title = title
        else:
            self.title =t.makeTextAI(f"give me a title for children book with a description of {description} {extra_promt}")

        story = t.makeTextAI(f'''
    You are currently a children's writer who is required to write a children's book about {subject}
    You are required to write {numPages} pages with each page no more than 30 words
    Return the respond as follow:
    Page 1: Text of page 1
    Page 2: Text of page 2
    And so on
    ''')
            
        print (f"story  = {story}")
        pages_text = storyTextSplit(story)    
        
        for i in range(numPages):

            steps  =imageQuality[quality_images].value 

            inputText = f'make an image ai promt for children story according to this text {pages_text[i]}'
            inputText = t.makeTextAI(inputText)
            pathImage = imageAIMaker.makeImageAI(inputText , steps , height_images  , width_images , staticNumIdPic)
            staticNumIdPic+=1
            voice_file_url =None
            if make_voice:
                voice_file_url = newVoiceFile(pages_text[i],f"{title}_page{i}_voice")
            self.pages.append(page(pages_text[i] , pathImage,voice_file_url)) 

    def to_dict(self):
        print(f"to_dict called: num pages = {len(self.pages)}")  

        dict = {
            'numPages': self.numPages,
            'auther': self.auther,
            'description': self.description,
            'title': self.title
        }
        pages_dict = [page.to_dict() for page in self.pages]
        dict['pages'] = pages_dict
        return dict
    
    def change_page_text(self, num_page,  new_text):
        self.pages[num_page].set_text_page(new_text)
    
    def change_page_text_ai(self, num_page , description):
        old_text = self.pages[num_page].get_text_page()
        extra_promt = " , just print the answer"
        promt = f"improve the old text: {old_text} description = {description}"
        self.pages[num_page].set_text_page()
    
# 
# story object: a python dict where every object has text and url to photo
 
# example:

#TODO: make python dic example 


class Continued_story(Story):
    def __init__(self,numPages, auther, description, title, staticNumIdPic 
                 ,previous_book_pages  ,previous_book_title
                 ,height_images=1080, width_images=1080, quality_images='MEDIUM', make_voice=True ):
        #part 1 finds out what the previous story was
        previous_book_story = previous_book_title +"\n"
        for page_bool_previous in previous_book_pages:
            previous_book_story += page_bool_previous.get('text_page')
            previous_book_story +='\n'

        #part 2 make the story for the current book

        self.numPages = numPages
        self.description = description
        self.auther =auther
        story = ''
        extra_promt = " , just print the answer"
        self.pages = []
        if title!= '':
            self.title = title
        else:
            self.title =t.makeTextAI(f"give me a title for children book with a description of {description} {extra_promt}")

        story = t.makeTextAI(f'''
    You are currently a children's writer who is required to write a children's book 
    You are making a sequel story, here is the text of the previous story: {previous_book_story}
    You are required to write {numPages} pages with each page no more than 30 words
    Return the respond as follow:
    Page 1: Text of page 1
    Page 2: Text of page 2
    And so on
    ''')
            
        print (f"story  = {story}")
        pages_text = storyTextSplit(story)    
        
        #part 3 make the current story pages (text and img url)
        for i in range(numPages):

            steps  =imageQuality[quality_images].value 

            inputText = f'make an image ai promt for children story according to this text {pages_text[i]}'
            inputText = t.makeTextAI(inputText)
            url_image = ''
            if i < len(previous_book_pages):
                url_image  = previous_book_pages[i]["img_url"]
            else:
                page_number = randint(0,len(previous_book_pages)-1)
                url_image  = previous_book_pages[page_number]["img_url"]
            pathImage = imageAIMaker.makeImageFromImage(inputText , steps , height_images  , width_images , staticNumIdPic, url_image)
            staticNumIdPic+=1
            voice_file_url =None
            if make_voice:
                voice_file_url = newVoiceFile(pages_text[i],f"{title}_page{i}_voice")
            self.pages.append(page(pages_text[i] , pathImage,voice_file_url)) 




