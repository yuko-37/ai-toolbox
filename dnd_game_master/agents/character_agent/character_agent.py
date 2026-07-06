import uuid
import logging

from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from mcp.client.streamable_http import streamable_http_client
from strands import Agent, tool
from strands.multiagent.a2a import A2AServer
from strands.tools.mcp.mcp_client import MCPClient
from tinydb import TinyDB, Query
from strands.models.ollama import OllamaModel
from dotenv import load_dotenv
from logging_config import setup_logging
from strands.telemetry import StrandsTelemetry
from random import randint


strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()

load_dotenv()
setup_logging()
logger = logging.getLogger('CharacterA2AServer')
logging.getLogger("strands").setLevel(logging.DEBUG)


@dataclass
class Stats:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

@dataclass
class InventoryItem:
    item_name: str
    quantity: int

@dataclass
class Character:
    character_id: str
    name: str
    character_class: str  # "class" is reserved in Python too
    race: str
    gender: str
    level: int
    experience: int
    stats: Stats
    inventory: List[InventoryItem]
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

characters_db = TinyDB('characters.json', indent=4, separators=(',', ': '))
Character_Query = Query()


@tool
def find_character_by_name(name: str) -> str:
    """
    Find a character by name
    
    Args:
        name: The character's name to search for
    """
    print(f"🔍 Searching for character with name: '{name}'")
    result = characters_db.search(Character_Query.name == name)
    
    if not result:
        print(f"❌ Character with name '{name}' not found")
        return f":x: Character with name '{name}' not found"
    
    character = result[0]
    print(f"✅ Found character: {character['name']} (ID: {character['character_id']}, {character['character_class']} {character['race']})")
    return character


@tool
def list_all_characters() -> str:
    """
    List all characters in the database
    """
    print("📋 Listing all characters in database")
    all_chars = characters_db.all()
    
    if not all_chars:
        print("❌ No characters found in database")
        return ":scroll: No characters found in the database"

    print(f"✅ Found {len(all_chars)} character(s) in database")
    for char in all_chars:
        print(f"  - {char['name']} ({char['character_class']} {char['race']})")
    
    return all_chars


def generate():
    values = [randint(1, 6) for _ in range(4)]
    result = sum(values) - min(values)
    return result


@tool(inputSchema={
    "json": {
        "type": "object",
        'properties': {
            'name': {'description': "Character's name", 'type': 'string'},
            'character_class': {'description': 'D&D class (Fighter, Wizard, etc.)', 'type': 'string'},
            'race': {'description': 'D&D race (Human, Elf, etc.)', 'type': 'string'},
            'gender': {'description': "Character's gender", 'type': 'string'},
            'stats_dict': {
                "type": "object",
                "description": 'Dictionary with abilities. If not provided, do not pass stats_dict',
                "properties": {
                    "strength": { "type": "integer" },
                    "dexterity": { "type": "integer" },
                    "constitution": { "type": "integer" },
                    "intelligence": { "type": "integer" },
                    "wisdom": { "type": "integer" },
                    "charisma": { "type": "integer" }
                },
                "required": ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
            }
        },

    'required': ['name', 'character_class', 'race', 'gender']
    }
})
def create_character(
    name: str,
    character_class: str,
    race: str,
    gender: str,
    stats_dict: Optional[Dict[str, int]] = None
    ) -> str:
    """
    Character details respecting the GameCharacters object fields.
    
    Args:
        name: Character's name
        character_class: D&D class (Fighter, Wizard, etc.)
        race: D&D race (Human, Elf, etc.)
        gender: Character's gender
        stats_dict: Dictionary with strength, dexterity, constitution, intelligence, wisdom, charisma

    Example:
        {'name': 'character_name',
         'character_class': 'Bard',
         'race': 'Human',
         'gender': 'Male',
         'stats_dict': {"strength": 14, "dexterity": 18, "constitution": 21, "intelligence": 5, "wisdom": 8, "charisma": 13}
        }
    """

    character_id = str(uuid.uuid4())
    if stats_dict is None:
        stats_dict = {}
    stats = Stats(
        strength=stats_dict.get('strength', generate()),
        dexterity=stats_dict.get('dexterity', generate()),
        constitution=stats_dict.get('constitution', generate()),
        intelligence=stats_dict.get('intelligence', generate()),
        wisdom=stats_dict.get('wisdom', generate()),
        charisma=stats_dict.get('charisma', generate()),
    )

    character = Character(
        character_id=character_id,
        name=name,
        character_class=character_class,
        race=race,
        gender=gender,
        level=1,
        experience=0,
        stats=stats,
        inventory=[
            InventoryItem("Starting Equipment Pack", 1),
            InventoryItem("Gold Pieces", 100)
        ]
    )

    logger.info("CHARACTER SUCCESSFULLY CREATED")
    # characters_db.insert(asdict(character))
    return character


DESCRIPTION="""
Specialized D&D character management agent that handles character creation, storage, and retrieval. 
Creates new characters, manages character data in persistent storage, 
and provides character lookup services.
"""

SYSTEM_PROMPT="""
You are a D&D character management specialist. 
Use the appropriate tools to create, find, or list characters as requested. Provide clear confirmations 
when characters are created and helpful summaries when characters are found. Keep responses focused and include 
relevant character details like class, race, and key stats."
"""


model = OllamaModel(host="http://localhost:11434", model_id="qwen3.5",
                        additional_args={"think": True})

agent = Agent(
    model=model,
    tools = [find_character_by_name, list_all_characters, create_character],
    name = "Character Creator Agent",
    description= DESCRIPTION,
    system_prompt= SYSTEM_PROMPT,
)


a2a_server = A2AServer(agent=agent, port=8001, enable_a2a_compliant_streaming=False)


if __name__ == "__main__":
    logger.info('Starting Character A2A Server...')
    a2a_server.serve()
