import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from PIL import ImageFilter
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image
import memoryManager
from qualityEnum import fileType

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
    return memoryManager.save_file(fileName ,fileType.png)

#TODO test this func
def make_mutiple_ai_images(prompts :list, steps, height, width, idPictuere):
        model_id = "stabilityai/stable-diffusion-2"

        scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
        pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")

        # Extend each prompt with quality suffix
        prompts = [prompt + ", 8K" for prompt in prompts]

        # Generate images in batch
        output = pipe(
            prompt=prompts,
            negative_prompt=["extra limbs, missing arms, missing legs, bad anatomy, low quality, blurry"] * len(prompts),
            height=height,
            width=width,
            guidance_scale=9.5,
            num_inference_steps=steps
        )

        file_urls = []
        for idx, image in enumerate(output.images):
            image = image.filter(ImageFilter.DETAIL)
            file_name = f"image_{idx}.png"
            image.save(file_name)
            print(f"Saved image {idx} as {file_name}")
            url = memoryManager.save_file(file_name, fileType.png)
            file_urls.append(url)

        return file_urls

def makeImageFromImage(prompt, steps, height, width, idPictuere , url_image_source):
    pipeline = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )
    pipeline.enable_model_cpu_offload()

    init_image = load_image(url_image_source).convert("RGB")

    # pass prompt and image to pipeline
    image = pipeline(prompt, 
                    image=init_image,
                    height = height,
                    width = width, 
                    strength=0.9).images[0] ## More creative divergence from source
    print("making image complete ")
    fileName  = f'image {idPictuere}.png'
    image = image.filter(ImageFilter.DETAIL)
    image.save(fileName)
    print(f"image saved as {fileName}")
    return memoryManager.save_file(fileName ,fileType.png)
     



