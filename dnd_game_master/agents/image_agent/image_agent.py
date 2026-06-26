import  logging
import re

from ollama import chat
from pydantic import BaseModel
from openai import OpenAI


class Filename(BaseModel):
    value: str


class ImageAgent:

    @staticmethod
    def sanitize_filename(name: str) -> str:
        name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name)
        return name.strip().strip('.')

    @staticmethod
    def generate_image_name(prompt: str) -> str:
        filename = ''
        message = (f"Based on the following description, generate a unique short filename.\nDescription:{prompt}.\ "
                   f"Return created filename in JSON format. \
                   Examples: MysticHalfElf, Elvish Performer, Elven_Bard_Character_Portrait")
        messages = [{'role': 'user', 'content': message}]
        try:
            response = chat(
                model='llama3.2',
                messages=messages,
                format=Filename.model_json_schema(),
            )
            generated_value = Filename.model_validate_json(response['message']['content']).value
            filename = ImageAgent.sanitize_filename(generated_value)[:50]
        except Exception as e:
            logging.error('Failed to generate image name', e)

        result = filename or 'default'
        logging.info(f'Image name generated: {result}')
        return result

    def generate_image(self, prompt: str) -> str:
        image_filename = self.generate_image_name(prompt)
        return f"file:///Users/yuko/MyFiles/dnd-images/{image_filename}.png"

        try:
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
            return url
        except Exception as e:
            raise ValueError("Failed to generate image", e)
