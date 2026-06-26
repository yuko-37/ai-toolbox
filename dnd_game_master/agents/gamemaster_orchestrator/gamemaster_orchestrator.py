import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tinydb import TinyDB, Query
from dotenv import load_dotenv
from logging_config import setup_logging
from logging import getLogger, INFO
from gamemaster_agent import get_gamemaster_agent


load_dotenv()
setup_logging()
logger = getLogger('GameMasterOrchestrator')
logger.setLevel(INFO)

agent = get_gamemaster_agent()
app = FastAPI(title="D&D Game Master API")
origins = ["https://aws-samples.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/messages")
def get_messages():
    return agent.messages


@app.get("/user/{user_name}")
def get_user(user_name):
    characters_db = TinyDB('./../character_agent/characters.json')
    Character_Query = Query()
    result = characters_db.search(Character_Query.name == user_name)
    if not result:
        return f":x: Character with name '{user_name}' not found"
    
    character = result[0]
    logger.info(f"✅ Found character: {character['name']} (ID: {character['character_id']}, {character['character_class']} {character['race']})")
    return character


@app.post("/inquire")
async def ask_agent(request: QuestionRequest):
    logger.info("Processing request...")
    try:
        response = await agent.invoke_async(request.question)
        logger.info(response.structured_output)
        return JSONResponse(content={ "response": response.structured_output.model_dump()})
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)


if __name__ == "__main__":
    logger.info("Starting GameMasterOrchestrator...")
    uvicorn.run(app, port=8009)
