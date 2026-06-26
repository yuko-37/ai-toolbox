import re
import base64

from ollama import chat
from pydantic import BaseModel
from openai import OpenAI
from io import BytesIO
from PIL import Image
from logging import getLogger


logger = getLogger("ImageAgent")


class Filename(BaseModel):
    value: str


class ImageAgent:

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name)
        return name.strip().strip('.')

    @staticmethod
    def _generate_image_name(prompt: str) -> str:
        filename = ''
        message = (f"Based on the following description, generate a unique short filename.\nDescription:{prompt}. \
                    Return created filename in JSON format. \
                   Examples: MysticHalfElf, Elvish Performer, Elven_Bard_Character_Portrait")
        messages = [{'role': 'user', 'content': message}]
        try:
            response = chat(
                model='llama3.2',
                messages=messages,
                format=Filename.model_json_schema(),
            )
            generated_value = Filename.model_validate_json(response['message']['content']).value
            filename = ImageAgent._sanitize_filename(generated_value)[:50]
        except Exception as e:
            logger.error('Failed to generate image name', e)

        result = filename or 'default'
        logger.info(f'Image name generated: {result}')
        return result

    @staticmethod
    def _generate_image_data(prompt: str) -> bytes:
        try:
            gpt = OpenAI()
            response = gpt.images.generate(
                model="gpt-image-1-mini",
                prompt=f"{prompt}. Use fantasy art style.",
                size="1024x1024",
                n=1
            )
            image_data = base64.b64decode(response.data[0].b64_json)
            return image_data
        except Exception as e:
            raise ValueError("Failed to generate image", e)

    @staticmethod
    def process_request(prompt: str) -> str:
        logger.info('Getting prompt: \n %s', prompt)

        logger.info('Creating name...')
        image_filename = ImageAgent._generate_image_name(prompt)
        # image_filename = 'stub-filename'
        logger.info('Name created: %s', image_filename)

        logger.info('Generating image...')
        image_data = ImageAgent._generate_image_data(prompt)
        img = Image.open(BytesIO(image_data))

        url = f"/Users/yuko/MyFiles/dnd-images/{image_filename}.png"
        logger.info('Saving image to file file://%s', url)
        img.save(url)

        return url
