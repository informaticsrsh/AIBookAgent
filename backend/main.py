from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/api/count")
async def count_characters(message: Message):
    return {"count": len(message.text)}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
