import textMaker as t
import imageAIMaker 
import re
from qualityEnum import imageQuality

def storyTextSplit(text):
    matches = re.split(r'Page \d+:\s', text)
    # Remove the first empty string if it exists, and strip whitespace
    arr = [page.strip() for page in matches if page.strip()]
    print(arr)
    return arr

class page():
    def __init__(self , text_page, img_url):
        self.text_page = text_page
        self.img_url = img_url
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
            'img_url': self.img_url
        }

    


class Story():
    def __init__(self , subject , numPages , auther , description , title ,
                  staticNumIdPic,height_images = 1080 , width_images = 1080 , 
                  quality_images = 'MEDIUM'  ):
        
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
            self.pages.append(page(pages_text[i] , pathImage)) 

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
        promt = f"improve the old text {old_text} {description}{old_text}"
        self.pages[num_page].set_text_page()
    
    
       


