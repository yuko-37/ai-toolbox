import base64
import logging

from openai import OpenAI
from PIL import Image
from io import BytesIO
from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.models.anthropic import AnthropicModel
from strands.multiagent.a2a import A2AServer
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()


@tool
def generate_scene_image(description: str, image_filename: str,
                         style: str = "fantasy art") -> str:
    """
    Generate an image to visualize the current scene or character.

    Args:
        description: Detailed description of what to visualize
        image_filename: A proper name for generated image
        style: Art style (fantasy art, medieval, dark fantasy, etc.)

    Returns:
        URL or path to the generated image
    """
    gpt = OpenAI()
    response = gpt.images.generate(
        model="gpt-image-1-mini",
        prompt=f"{description}. Use {style} style.",
        size="1024x1024",
        n=1
    )
    image_data = base64.b64decode(response.data[0].b64_json)
    img = Image.open(BytesIO(image_data))
    url = f"/Users/yuko/MyFiles/dnd-images/{image_filename}.png"
    img.save(url)
    return urls

DESCRIPTION="""
An image generation agent. Generates image and provides url to the generated content.
Take into consideration that image generation can be slow.
"""

SYSTEM_PROMPT="""
You are responsible for image generation. You must create a comprehensive prompt 
describing current game scene or character. You must create a proper name for the image.
Use the created prompt for image generation model 
and pass it and create filename to the image generation tool.
"""

model = AnthropicModel(model_id="claude-haiku-4-5-20251001", max_tokens=1000)

agent = Agent(
    model=model,
    tools=[generate_scene_image],
    name='Image Creator Agent',
    description=DESCRIPTION,
    system_prompt=SYSTEM_PROMPT
)

a2a_server = A2AServer(agent=agent, port=8002)


if __name__ == "__main__":
    a2a_server.serve()