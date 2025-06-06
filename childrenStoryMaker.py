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

    def __init__(
        self,
        subject: str,
        numPages: int,
        auther: str,
        description: str,
        title: str,
        pages_texts_list:  list |None,
        make_voice: bool):
        
        # no text inclued = complete AI story
        if len(pages_texts_list)==0:
           self.AI_story_maker(subject,numPages,auther,description,title,make_voice)
        #pages= story from the user 
        else:
            print("making a new story , pages has been have by the user.")
            self.story_media_maker(subject,numPages,auther,description,title,make_voice,pages_texts_list)
        print("story has been complete \n\n")

    def story_media_maker(
            self ,
            subject: str,
            numPages: int,
            auther: str,
            description: str,
            title: str,
            make_voice : bool,
            pages_texts_list : list):
        
        self.numPages = numPages
        self.description = description
        self.auther =auther
        extra_promt = " , just print the answer"
        self.pages = []
        if title!= '':
            self.title = title
        else:
            self.title =t.makeTextAI(f"give me a title for children book with a description of {description} {extra_promt}")
        #no rellevant: move from  stable diffusion to gemini
        #steps  =imageQuality[quality_images].value 
        #save value of the first image to base the rest of the images on that
        url_first_image =''
        images_prompts =[]
        for i in range(numPages):

            inputText = f'make an image prompt for children story according to this text not longer then 15 words {pages_texts_list[i]} , the subject of the story :{subject} '
            if (i>0):
                previous_story_pages = ' '.join([prompt for prompt in images_prompts])
                inputText += f'\n making sure to maintain consistent visual elements such as [clothing, colors, background, art style, recurring objects]. The image should reflect a coherent world and preserve recurring elements seen in previous images. Focus on [relevant features , e.g., expression, background setting, lighting]. \n here is the previous story pages images prompts for refrence: {previous_story_pages}'
            
            print(inputText)

            inputText = t.makeTextAI(inputText)
            print(f"\n\n input prompt for image {i} in the story : {inputText}\n\n")
            pathImage = None
            if i==0:
                #pathImage = f"{title}_page{i}_pic"
                pathImage = imageAIMaker.makeImageAI(inputText)
                url_first_image = str(pathImage)
            else:
                
                #pathImage = f"{title}_page{i}_pic"
                pathImage = imageAIMaker.makeImageFromImage(inputText ,url_first_image)
            
            images_prompts.append(inputText)

            #no rellevant: move from  stable diffusion to gemini
            #pathImage = imageAIMaker.makeImageAI(inputText , steps , height_images  , width_images , staticNumIdPic)
            #staticNumIdPic+=1
            voice_file_url = None
            if make_voice:
                voice_file_url = newVoiceFile(pages_texts_list[i],f"{title}_page{i}_voice")
            self.pages.append(page(pages_texts_list[i] , pathImage,voice_file_url)) 

        

    def AI_story_maker(
            self ,
            subject: str,
            numPages: int,
            auther: str,
            description: str,
            title: str,
            make_voice : bool):
        
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
    You are required to write {numPages} pages with each page no more than 150 words
    Return the respond as follow:
    Page 1: Text of page 1
    Page 2: Text of page 2
    And so on
    ''')
            
        print (f"story  {story}")
        pages_text = storyTextSplit(story) 
        
        #no rellevant: move from  stable diffusion to gemini
        #steps  =imageQuality[quality_images].value 
        
        
        #save value of the first image to base the rest of the images on that
        url_first_image =''
        for i in range(numPages):

            inputText = f'make an image prompt for children story according to this text not longer then 15 words {pages_text[i]}'
            inputText = t.makeTextAI(inputText)
            pathImage = None
            if i==0:
                pathImage = imageAIMaker.makeImageAI(inputText)
                url_first_image = str(pathImage)
            else:
                pathImage = imageAIMaker.makeImageFromImage(inputText ,url_first_image)
            #no rellevant: move from  stable diffusion to gemini
            #pathImage = imageAIMaker.makeImageAI(inputText , steps , height_images  , width_images , staticNumIdPic)
            #staticNumIdPic+=1
            voice_file_url = None
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
    

    


class Continued_story(Story):
    def __init__(self,numPages, auther, description, title
                 ,previous_book_pages  ,previous_book_title
                , make_voice=True ):
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
    You are required to write {numPages} pages with each page no more than 150 words
    Return the respond as follow:
    Page 1: Text of page 1
    Page 2: Text of page 2
    And so on
    ''')
            
        print (f"story  = {story}")
        pages_text = storyTextSplit(story)    
        
 
        #save value of the first image to base the rest of the images on that
        url_first_image =''
        for i in range(numPages):

            inputText = f'make an image prompt for children story according to this text not longer then 15 words {pages_text[i]}'
            inputText = t.makeTextAI(inputText)
            while (len(inputText )>50):
                inputText = f'make an image ai prompt for children story according to this text not longer then 15 words {pages_text[i]}'
                inputText = t.makeTextAI(inputText)
            pathImage = None
            if i==0:
                pathImage = imageAIMaker.makeImageAI(inputText)
                url_first_image = str(pathImage)
            else:
                pathImage = imageAIMaker.makeImageFromImage(inputText ,url_first_image)
            #no rellevant: move from  stable diffusion to gemini
            #pathImage = imageAIMaker.makeImageAI(inputText , steps , height_images  , width_images , staticNumIdPic)
            #staticNumIdPic+=1
            voice_file_url = None
            if make_voice:
                voice_file_url = newVoiceFile(pages_text[i],f"{title}_page{i}_voice")
            self.pages.append(page(pages_text[i] , pathImage,voice_file_url)) 





