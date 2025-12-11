from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from gemini_service import GeminiService
import asyncio
import json

app = FastAPI()
gemini_service = GeminiService()

is_debate_active = False
chat_history = []

class ChatMessage(BaseModel):
    text: str
    api_key: str

class DebateMessage(BaseModel):
    topic: str
    api_key: str
    agent_a_role: str
    agent_b_role: str
    flash_rpm: int
    pro_rpm: int

@app.post("/api/chat")
async def chat(message: ChatMessage):
    if not message.api_key:
        raise HTTPException(status_code=400, detail="API Key is missing. Please configure it in settings.")

    try:
        response_text = gemini_service.generate_flash_response(message.api_key, message.text)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/debate")
async def debate(message: DebateMessage):
    global is_debate_active, chat_history
    if is_debate_active:
        raise HTTPException(status_code=400, detail="A debate is already in progress.")

    is_debate_active = True
    chat_history = [{"sender": "User", "text": message.topic}]
    gemini_service.flash_rpm = message.flash_rpm
    gemini_service.pro_rpm = message.pro_rpm
    asyncio.create_task(debate_loop(message.api_key, message.topic, message.agent_a_role, message.agent_b_role))
    return {"status": "Debate started."}

@app.post("/api/stop")
async def stop_debate():
    global is_debate_active
    is_debate_active = False
    return {"status": "Debate stopped."}

@app.get("/api/history")
async def get_history():
    return {"history": chat_history}

async def debate_loop(api_key: str, topic: str, agent_a_role: str, agent_b_role: str):
    global is_debate_active, chat_history

    while is_debate_active:
        # Agent A (Flash)
        history_str = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in chat_history])
        response_a = gemini_service.generate_flash_response(api_key, history_str, system_instructions=agent_a_role)
        if not is_debate_active: break
        chat_history.append({"sender": "Agent A", "text": response_a})

        await asyncio.sleep(1)

        # Agent B (Pro)
        history_str = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in chat_history])
        response_b = gemini_service.generate_pro_response(api_key, history_str, system_instructions=agent_b_role)
        if not is_debate_active: break
        chat_history.append({"sender": "Agent B", "text": response_b})

        await asyncio.sleep(1)


app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
