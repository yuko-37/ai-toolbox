#!/usr/bin/env python
import warnings

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

requirements = """
A system is a chat with coach AI assistant with benefits.
The system should allow user to input message via textbox by typing and via microphone.
The user message then is passed to coach AI assistant to get response.
At the same time the user message is send to another LLM to get evaluation of the message from english natural phasing point of view.
On one tab user can see its conversation in chat with coach AI assistant.
On second tab user can see the result of its english message evaluation.
AI coach response should be independent of evaluation.
English evaluation tab should include original message, corrected by LLM message and 1-3 essential notes regarding english natural phasing.
The system should allow user to choose model behind coach AI assistant.
The system should allow user to choose model behind english evaluation.
The system should load the list of possible model values from model.json
Example of LLM models: gpt-5-nano, gpt-4o-mini, gpt-5.4-mini, llama3.2
The system should allow the user to set system instruction for AI assistant.
The system should allow the user to set system instruction for english evaluation.
The system should remember the user's chosen models
The system should remember the user's last set system instructions
"""
module_name = "coach.py"
class_name = "Coach"


def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
    }

    try:
        EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
