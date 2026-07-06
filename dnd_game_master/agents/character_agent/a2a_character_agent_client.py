import logging
import sys

from strands.agent.a2a_agent import  A2AAgent


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

a2a_agent = A2AAgent(endpoint="http://127.0.0.1:8001")

message = """
Create a new player named yuko who is a Female Half-Elf Bard and abilities:
strength=14, dexterity=18, constitution=21, intelligence=5, wisdom=8, charisma=13
"""

# message = """
# Create a new player named yuko who is a Female Half-Elf Bard
# """

def send_request(request):
    result = a2a_agent(request)
    return result

resp = send_request(message)
print(resp)
