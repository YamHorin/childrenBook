import torch
from torchvision.utils import save_image
from diffusers import StableDiffusionPipeline  , DPMSolverMultistepScheduler
import requests
import json
import sys
sys.stdout.flush()

# Load pipeline once
small_model = "stabilityai/stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(small_model, torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_attention_slicing()
pipe = pipe.to("cuda")

def makeImage(prompts, batch_size=2, steps=75, scale=7.5, height=768, width=768):
    images = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        results = pipe(
            batch,
            num_inference_steps=steps,
            guidance_scale=scale,
            height=height,
            width=width
        )
        images.extend(results.images)
    for i, img in enumerate(images):
        img.save(f"image_{i}.png")
    


prompts = [
    "a programmer touching grass",
    "A dreamlike landscape with floating islands and waterfalls under a starry sky.",
    "A Roman soldier standing guard in front of the Colosseum during sunset.",
    "A cyberpunk character with neon tattoos in a rain-soaked alley."
]
makeImage(prompts)