import os

from strands import Agent
from strands.handlers import null_callback_handler
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamable_http_client
from strands_tools.a2a_client import A2AClientToolProvider
from strands.models.anthropic import AnthropicModel
from strands.models.ollama import OllamaModel
from pydantic import BaseModel, Field
from logging import getLogger, INFO
from typing import List, Optional


logger = getLogger("GameMasterAgent")
logger.setLevel(INFO)


SYSTEM_PROMPT = """You are a D&D Game Master orchestrator with access to specialized agents and tools.

Available agents:
- Use Rules Agent for D&D mechanics and rules
- Use Character Agent for character creation and management

To communicate with agents:
1. Use a2a_list_discovered_agents to see available agents
2. Use a2a_send_message with the agent's URL to send questions
3. Use roll_dice for dice rolling

Available D&D dice types:
- d4 (4-sided die) - Used for damage rolls of small weapons like daggers
- d6 (6-sided die) - Used for damage rolls of weapons like shortswords, spell damage
- d8 (8-sided die) - Used for damage rolls of weapons like longswords, rapiers
- d10 (10-sided die) - Used for damage rolls of heavy weapons, percentile rolls
- d12 (12-sided die) - Used for damage rolls of great weapons like greataxes
- d20 (20-sided die) - Used for ability checks, attack rolls, saving throws
- d100 (percentile die) - Used for random tables, wild magic surges

IMPORTANT: Always use the exact URLs shown by a2a_list_discovered_agents. Never invent or guess URLs.

Be creative, engaging, and use your available tools to enhance the D&D experience.
"""


class DiceOutput(BaseModel):
    dice_type: str = Field(description="The dice type. Ex: d4, d6, d20, etc")
    result: int = Field(description="The dice result value alone")
    reason: str = Field(description="The reason the dice was rolled. Ex: attack roll. And the modificators if there was any")


class StoryOutput(BaseModel):
    """Model that contains information about a Person"""
    response: str = Field(description="Your narrative response as Game Master")
    actions_suggestions: list[str] = Field(description="['Action 1', 'Action 2', 'Action 3']")
    details: str = Field(description="Brief summary of tools/agents used")
    dice_rolls: Optional[List[DiceOutput]] = Field(default=[], description="List of dice rolls with dice_type, result, and reason")


A2A_AGENT_URLS = [
    "http://localhost:8000",
    "http://localhost:8001",
]

MCP_SERVER_URL = "http://localhost:8080/mcp"


def get_gamemaster_agent():
    try:
        mcp_client = MCPClient(lambda: streamable_http_client(MCP_SERVER_URL))
        a2a_client = A2AClientToolProvider(known_agent_urls=A2A_AGENT_URLS)
        model = OllamaModel(model_id='qwen3.5', host="http://localhost:11434", additional_args={"think": "low"})
        logger.info(f'Set GameMasterAgent model: {type(model)}')

        agent = Agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=[mcp_client] + a2a_client.tools,
            structured_output_model=StoryOutput,
        )

    except Exception as e:
        raise Exception(f"Error while GameMasterAgent initialization:", e)

    return agent
