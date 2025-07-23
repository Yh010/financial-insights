from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from app.functions.gemini import generate
from app.functions.extractor import extract
import re, json
from app.rag_test.prepare_corpus_and_data import upload_files_to_rag_corpus
from app.rag_test.agent import router as rag_test_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.post("/gemini")
def gemini(user_prompt: str = Form(...), images: List[UploadFile] = File(None)):
    image_bytes_list = [image.file.read() for image in images] if images else []
    response = generate(user_prompt, image_bytes_list)
    return {"response": response} 

@app.post("/extract")
def gemini(images: List[UploadFile] = File(None)):
    image_bytes_list = [image.file.read() for image in images] if images else []
    response = extract(image_bytes_list)
    # Clean up response: remove code block markers and parse JSON
    # Remove code block markers and any leading/trailing whitespace
    cleaned = re.sub(r"^```json|^```|```$", "", response.strip(), flags=re.MULTILINE).strip()
    # Try to parse as JSON
    try:
        parsed = json.loads(cleaned)
    except Exception:
        parsed = cleaned  # fallback: return raw if not valid JSON
    return parsed 

@app.post("/rag/upload")
def rag_upload(files: List[UploadFile] = File(...)):
    uploaded = upload_files_to_rag_corpus(files)
    return {"uploaded": uploaded} 

app.include_router(rag_test_router) 
