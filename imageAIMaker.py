import memoryManager
import requests
from qualityEnum import fileType

#version 1 with satble diffusion ,  imports not rellevent
# import torch
# from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
# from PIL import ImageFilter
# from diffusers import AutoPipelineForImage2Image
# from diffusers.utils import load_image

import uuid
from io import BytesIO
from google import genai
from os import getenv
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv


# #version 1 with satble diffusion , not rellevent
def makeImageAI(prompt, steps, height, width, idPictuere):
    model_id = "stabilityai/stable-diffusion-2"

    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(   prompt = prompt +",cartoon,children story style,8K",
                    negative_prompt="extra heads,extra limbs, missing arms, missing legs, bad anatomy, low quality, blurry",
                    height = height,
                    width = width,
                    guidance_scale=9.5,
                    num_inference_steps=steps
                ).images[0]
    print("making image complete ")
    fileName  = f'image {idPictuere}.png'
    image = image.filter(ImageFilter.DETAIL)
    image.save(fileName)
    print(f"image saved as {fileName}")
    return memoryManager.save_file(fileName ,fileType.png)

#version 2 with google gemini

def makeImageAI(promt):
    load_dotenv(override= True)
    apiKey = getenv("API_KEY")
    client = genai.Client(api_key=apiKey)

    contents = (promt)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )
    picInclude = False
    #make random image name
    idPictuere = str(uuid.uuid4())[1:6]
    fileName  = f'image {idPictuere}.png'
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(fileName)
            print(f"image saved as {fileName}")
            picInclude =True
    if picInclude :
        return memoryManager.save_file(fileName ,fileType.png)
    else:
        return None

# # #version 1 Stable Diffusion not Rellvant
def makeImageFromImage(prompt, steps, height, width, idPictuere , url_image_source):
    pipeline = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )
    pipeline.enable_model_cpu_offload()

    # Load image from URL
    response = requests.get(url_image_source)
    response.raise_for_status()  # Raise an error for bad responses
    init_image = Image.open(BytesIO(response.content)).convert("RGB")


    
    # pass prompt and image to pipeline
    image = pipeline(prompt, 
                    image=init_image,
                    height = height,
                    width = width, 
                    strength=0.7).images[0] ## More creative divergence from source
    print("making image complete ")
    fileName  = f'image {idPictuere}.png'
    image = image.filter(ImageFilter.DETAIL)
    image.save(fileName)
    print(f"image saved as {fileName}")
    return memoryManager.save_file(fileName ,fileType.png)

#version 2 google gemini

def makeImageFromImage(prompt  ,url_image_source):
    #apiKey

    load_dotenv(override= True)
    apiKey = getenv("API_KEY")
    client = genai.Client(api_key=apiKey)

    # Load image from URL
    response = requests.get(url_image_source)
    response.raise_for_status()  # Raise an error for bad responses
    image = Image.open(BytesIO(response.content)).convert("RGB")

    client = genai.Client(api_key=apiKey)

    text_input = (prompt)

    #file name
    idPictuere = str(uuid.uuid4())[1:6]
    fileName  = f'image {idPictuere}.png'

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )
    picInclude = False

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(fileName)
            print(f"image saved as {fileName}")
            picInclude = True
    if picInclude :
        return memoryManager.save_file(fileName ,fileType.png)
    else:
        return None


#version 1 Stable Diffusion not Rellvant

def makeImagesFromPrompts(prompts, steps, height, width, idPrefix, url_image_source):
    # Load the model once
    pipeline = AutoPipelineForImage2Image.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )
    pipeline.enable_model_cpu_offload()

    # Load source image from URL
    response = requests.get(url_image_source)
    response.raise_for_status()
    init_image = Image.open(BytesIO(response.content)).convert("RGB")

    urls = []

    for i, prompt in enumerate(prompts):
        print(f"Generating image for prompt {i + 1}/{len(prompts)}...")

        # Generate image from prompt
        image = pipeline(
            prompt,
            image=init_image,
            height=height,
            width=width,
            strength=0.9
        ).images[0]

        image = image.filter(ImageFilter.DETAIL)
        fileName = f'image_{idPrefix}_{i}.png'
        image.save(fileName)

        print(f"Image {i + 1} saved as {fileName}")
        image_url = memoryManager.save_file(fileName, fileType.png)
        urls.append(image_url)

    print("All images generated and saved.")
    return urls




