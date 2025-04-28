import torch
#from diffusers import StableDiffusion3Pipeline
from diffusers import StableCascadeDecoderPipeline, StableCascadePriorPipeline
from PIL import Image

from diffusers import StableDiffusionPipeline

# model_id = "sd-legacy/stable-diffusion-v1-5"
# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
# pipe = pipe.to("cuda")
# steps = 750 #max is 999
# prompt = "a photo of an astronaut riding a horse on mars in cartoon style"
# image = pipe(prompt = prompt,
#              guidance_scale=7.0,
#              num_inference_steps=steps).images[0]  
    
# image.save("astronaut_rides_horse.png")



from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3.5-medium")

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]
#version 0.2.0
# This version uses threading to save images asynchronously and reduces hardcoded steps

# Initialize models once
# prior = StableCascadePriorPipeline.from_pretrained(
#     "stabilityai/stable-cascade-prior", variant="bf16", torch_dtype=torch.bfloat16
# )
# decoder = StableCascadeDecoderPipeline.from_pretrained(
#     "stabilityai/stable-cascade", variant="bf16", torch_dtype=torch.bfloat16
# )

# staticNumImages = 0
# negative_prompt = ""  # Static value

# def save_image(image, name):
#     image.save(name)

# def makeImageAI(prompt, steps, height, width):
#     global staticNumImages
#     global negative_prompt
#     global prior
#     global decoder
#     # Generate prior output
#     prior_output = prior(
#         prompt=prompt,
#         height=height,
#         width=width,
#         negative_prompt=negative_prompt,
#         guidance_scale=4.0,
#         num_images_per_prompt=1,
#         num_inference_steps=steps  
#     )

#     # Generate decoder output
#     decoder_output = decoder(
#         image_embeddings=prior_output.image_embeddings.to(torch.float16),
#         prompt=prompt,
#         negative_prompt=negative_prompt,
#         guidance_scale=0.0,
#         output_type="pil",
#         num_inference_steps=10  # Reduce hardcoded steps
#     ).images[0]

#     # Save image asynchronously
#     nameFile = f'image{staticNumImages}.png'
#     threading.Thread(target=save_image, args=(decoder_output, nameFile)).start()
#     print(f'Image saved as {nameFile}')
#     staticNumImages += 1

#     return nameFile


