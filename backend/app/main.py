from fastapi import FastAPI, Query, Body
from pydantic import BaseModel
from app.functions.gemini import generate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

class GeminiRequest(BaseModel):
    user_prompt: str

@app.post("/gemini")
def gemini(request: GeminiRequest):
    response = generate(request.user_prompt)
    return {"response": response} 

