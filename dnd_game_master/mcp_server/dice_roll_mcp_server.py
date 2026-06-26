import random
import logging
import os
import sys

from mcp.server import FastMCP
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger('Dice Roll MCP Server')
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=os.getenv('LOG_FORMAT'))


mcp = FastMCP(
    name="D&D Dice Roll Service",
    port=8080
)

@mcp.tool()
def roll_dice(faces: int = 6, count: int = 1) -> dict:
    """
    🎲 Roll multiple dice with a specified number of faces.
    
    Args:
        faces: Number of faces on the dice (default: 6)
        count: Number of dice to roll (default: 1)
        
    Returns:
        Dictionary with list of results and faces
    """
    if faces < 1:
        error_msg = "Dice must have at least 1 face"
        logging.warning(f"🎲 Invalid dice roll request: {error_msg}")
        return {"error": error_msg}
    
    if count < 1:
        error_msg = "Must roll at least 1 dice"
        logging.warning(f"🎲 Invalid dice roll request: {error_msg}")
        return {"error": error_msg}
    
    results = [random.randint(1, faces) for _ in range(count)]

    logging.info(f"🎲 DICE ROLL: {count}d{faces} = {results}")
    
    return {
        "results": results,
        "faces": faces
    }


if __name__ == "__main__":
    logger.info("Starting D&D Dice Roll MCP Server...")
    mcp.run(transport="streamable-http")
