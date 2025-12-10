from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from gemini_service import GeminiService

app = FastAPI()
gemini_service = GeminiService()

class ChatMessage(BaseModel):
    text: str
    api_key: str

@app.post("/api/chat")
async def chat(message: ChatMessage):
    if not message.api_key:
        raise HTTPException(status_code=400, detail="API Key is missing. Please configure it in settings.")

    try:
        response_text = gemini_service.generate_text(message.api_key, message.text)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
