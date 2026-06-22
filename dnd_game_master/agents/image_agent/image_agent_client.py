import logging

from strands.agent.a2a_agent import A2AAgent


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

a2a_agent = A2AAgent(endpoint="http://127.0.0.1:8002")

message = """
Generate image for the Character.
Character Details:

Pointed elven ears with graceful half-elf heritage
Long dark wavy hair with silver clasps catching the firelight
Sharp, elegant cheekbones and captivating eyes with mischievous sparkle
Deep blue tunic with leather accents
Amber-polished lute ready for performance
Confident, charismatic stance
"""

result = a2a_agent(message)
