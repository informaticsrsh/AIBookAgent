from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os
import google.generativeai as genai

app = FastAPI()

def get_genai_model(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="API key is missing or invalid.")

    api_key = auth_header.split(" ")[1]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def read_manuscript_and_rules():
    manuscript_content = ""
    if os.path.exists(MANUSCRIPT_FILE):
        with open(MANUSCRIPT_FILE, "r") as f:
            manuscript_content = f.read()

    rules = ""
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as f:
            rules = f.read()

    return manuscript_content, rules

def save_manuscript(content):
    with open(MANUSCRIPT_FILE, "w") as f:
        f.write(content)

MANUSCRIPT_FILE = "manuscript.md"
RULES_FILE = "author_rules.txt"

@app.post("/save_rules")
async def save_rules(file: UploadFile = File(...)):
    with open(RULES_FILE, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": f"Rules file '{file.filename}' saved."}

@app.get("/get_book")
async def get_book():
    if not os.path.exists(MANUSCRIPT_FILE):
        with open(MANUSCRIPT_FILE, "w") as f:
            f.write("# Your Book Title\n\nStart writing here...")
    return FileResponse(MANUSCRIPT_FILE, media_type='text/markdown', filename="manuscript.md")

@app.post("/generate")
async def generate(request: Request, model: genai.GenerativeModel = Depends(get_genai_model)):
    try:
        data = await request.json()
        user_prompt = data.get("prompt")
        if not user_prompt:
            raise HTTPException(status_code=400, detail="Prompt not provided.")

        manuscript_content, rules = read_manuscript_and_rules()
        full_prompt = f"Continue the story based on the following manuscript:\n\n{manuscript_content}\n\nUser instruction: {user_prompt}"
        if rules:
            full_prompt = f"{rules}\n\n{full_prompt}"

        response = model.generate_content(full_prompt)
        newly_generated_text = response.text

        updated_manuscript = manuscript_content + "\n\n" + newly_generated_text
        save_manuscript(updated_manuscript)

        return {"message": newly_generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expand")
async def expand(request: Request, model: genai.GenerativeModel = Depends(get_genai_model)):
    try:
        manuscript_content, rules = read_manuscript_and_rules()
        prompt = f"Write a new passage that expands on the following story:\n\n{manuscript_content}"
        if rules:
            prompt = f"{rules}\n\n{prompt}"

        response = model.generate_content(prompt)
        newly_generated_passage = response.text

        updated_manuscript = manuscript_content + "\n\n" + newly_generated_passage
        save_manuscript(updated_manuscript)

        return {"message": newly_generated_passage}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"Hello": "World"}
