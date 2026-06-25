import logging
import os
import uvicorn

from dotenv import load_dotenv
from a2a.types import AgentSkill, AgentCard
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from image_agent_exectutor import ImageAgentExecutor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()


HOST = os.getenv('AGENTS_HOST')
PORT = int(os.getenv('IMAGE_AGENT_PORT'))


def main():
    image_generation_skill = AgentSkill(
        id='image_generation_skill',
        name='Image Generation Skill',
        description="Generates image based on given detailed description and return URL to the image.",
        tags=['image-generation'],
        examples=["""
    Generate image for the Character.
    Character Details:
    
    Pointed elven ears with graceful half-elf heritage
    Long dark wavy hair with silver clasps catching the firelight
    Sharp, elegant cheekbones and captivating eyes with mischievous sparkle
    Deep blue tunic with leather accents
    Amber-polished lute ready for performance
    Confident, charismatic stance
        """],
        input_modes=['text/plain'],
        output_modes=['text/uri-list']
    )

    image_agent_card = AgentCard(
        name="ImageGenerationAgent",
        description="Generates image based on given detailed description and return URL of the image.",
        url=f"http://{HOST}:{PORT}",
        version="1.0.0",

        capabilities={
            "streaming": False,
            "pushNotifications": True,
            "longRunningOperation": True
        },

        skills=[
            image_generation_skill
        ],
        default_input_modes=["text/plain"],
        default_output_modes=["text/uri-list"]
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ImageAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=image_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host=HOST, port=PORT)


if __name__ == '__main__':
    main()