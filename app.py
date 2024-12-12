import torch
from torchvision.utils import save_image
from diffusers import StableDiffusionPipeline
from ollama import chat
from ollama import ChatResponse

# Load the pre-trained Stable Diffusion model
def makeImages(prompt):
    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Use GPU for faster processing

    # Generate an image
    image = pipe(prompt).images[0]

    # Save the image
    image.save("output.png")
    print("Image saved as output.png")
    
def makeTextAi(prompt):
    response: ChatResponse = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    print(response['message']['content'])
    # or access fields directly from the response object
    print(response.message.content)

makeTextAi("make a story time for children not longer then 10 lines")