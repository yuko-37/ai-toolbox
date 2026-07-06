import logging
import sys
from idlelib.rpc import response_queue

import requests

from strands.agent.a2a_agent import  A2AAgent


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


message = """
Create a new player named yuko who is a Female Human Bard. You can then welcome them to the game.
Describe the surroundings of the player and create an atmosphere that the player can bounce off of.
Don't make more than 100 words.
"""

def send_request(request):
    response = requests.post("http://127.0.0.1:8009/inquire", json={"question": message})
    return response

resp = send_request(message)
print(resp)
