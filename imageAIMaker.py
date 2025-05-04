import torch
#from diffusers import StableDiffusion3Pipeline
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from diffusers import StableCascadeDecoderPipeline, StableCascadePriorPipeline
from PIL import ImageFilter

def makeImageAI(prompt, steps, height, width, idPictuere):
    model_id = "stabilityai/stable-diffusion-2"

    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(   prompt = prompt +",8K",
                    negative_prompt="extra limbs, missing arms, missing legs, bad anatomy, low quality, blurry",
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
    return fileName




