from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://*.lovableproject.com",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

    prompt = f"Suggest 3 pickup {req.sport} games someone could join in {req.location}"

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()
