from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()
origins = [
    "*"  # allow all domains; simpler for testing with Lovable
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # use "*" to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GameRequest(BaseModel):
    sport: str
    location: str

@app.get("/")
def home():
    return {"message": "Pickup Play backend running"}

@app.post("/find-games")
def find_games(req: GameRequest):

    prompt = f"""
    Suggest 3 pickup {req.sport} games someone could join in {req.location}.
    Return each game as a JSON object with fields: title, location, time, players.
    The output must be a JSON array.
    """ 
    
    url = "https://api/groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    # Call the LLM
    response = requests.post(url, headers=headers, json=data).json()

    # Extract the LLM text content
    content = response["choices"][0]["message"]["content"]

    # Parse the JSON safely
    import json
    try:
        games = json.loads(content)
    except json.JSONDecodeError:
        games = []  # fallback if parsing fails

    # Return in the format Lovable expects
    return {"games": games}
