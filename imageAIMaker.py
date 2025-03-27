import torch
from diffusers import StableDiffusionPipeline,DPMSolverMultistepScheduler
from PIL import Image

# Replace the model version with your required version if needed
pipeline = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16
)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
pipeline.enable_attention_slicing()
# Running the inference on GPU with cuda enabled
pipeline = pipeline.to('cuda')



prompt = "boy and girl are best friends in children book art style  "

image = image = pipeline(
    prompt=prompt,
    num_inference_steps=200,  # Increase steps for better quality
    guidance_scale=10.0,     # Adjust adherence to the prompt
    height=768,              # Custom height
    width=768,               # Custom width
).images[0]
image.show()