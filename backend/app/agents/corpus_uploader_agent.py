from google.adk import Agent
from app.rag_test.prepare_corpus_and_data import upload_user_documents_to_corpus
import tempfile
import os
from typing import Optional


def upload_extracted_text_to_corpus(text: str, filename: Optional[str] = None):
    # Save the extracted text to a temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        if not filename:
            filename = "extracted_data.txt"
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        uploaded = upload_user_documents_to_corpus([file_path])
    return {"uploaded": uploaded}

corpus_uploader_agent = Agent(
    model="gemini-2.5-pro",
    name="corpus_uploader_agent",
    instruction="You receive extracted text from documents and upload it to the RAG corpus for future retrieval.",
    output_key="corpus_uploader_output",
    tools=[upload_extracted_text_to_corpus],
) 