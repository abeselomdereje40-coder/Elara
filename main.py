from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from brain import Brain

app=FastAPI()
brain=Brain()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    session_id:str
    message:str

@app.get("/")
def home():
    return {
        "status":"online"
    }

@app.post("/chat")
def chat(data: Message):
    replay=brain.think(data.session_id, data.message)
    return {
       "replay":replay
    }