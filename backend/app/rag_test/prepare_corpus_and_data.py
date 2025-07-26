import os
from google.auth import default
import vertexai
from vertexai.preview import rag
from dotenv import load_dotenv, set_key

# Load environment variables from .env file
load_dotenv(dotenv_path="app/.env")

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it in your .env file.")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
if not LOCATION:
    raise ValueError("GOOGLE_CLOUD_LOCATION environment variable not set. Please set it in your .env file.")
CORPUS_DISPLAY_NAME = "User_Uploaded_Corpus"
CORPUS_DESCRIPTION = "Corpus containing user-uploaded documents."
ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
print(ENV_FILE_PATH);


def initialize_vertex_ai():
    credentials, _ = default()
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

def create_or_get_corpus():
    embedding_model_config = rag.EmbeddingModelConfig(
        publisher_model="publishers/google/models/text-embedding-004"
    )
    existing_corpora = rag.list_corpora()
    corpus = None
    for existing_corpus in existing_corpora:
        if existing_corpus.display_name == CORPUS_DISPLAY_NAME:
            corpus = existing_corpus
            print(f"Found existing corpus with display name '{CORPUS_DISPLAY_NAME}'")
            break
    if corpus is None:
        corpus = rag.create_corpus(
            display_name=CORPUS_DISPLAY_NAME,
            description=CORPUS_DESCRIPTION,
            embedding_model_config=embedding_model_config,
        )
        print(f"Created new corpus with display name '{CORPUS_DISPLAY_NAME}'")
    return corpus

def upload_user_documents_to_corpus(file_paths):
    """
    Uploads one or more user documents (local file paths) to the RAG corpus.
    """
    initialize_vertex_ai()
    corpus = create_or_get_corpus()
    set_key(ENV_FILE_PATH, "RAG_CORPUS", corpus.name)
    uploaded = []
    for file_path in file_paths:
        display_name = os.path.basename(file_path)
        print(f"Uploading {display_name} to corpus...")
        try:
            rag_file = rag.upload_file(
                corpus_name=corpus.name,
                path=file_path,
                display_name=display_name,
                description=f"User uploaded file: {display_name}"
            )
            print(f"Successfully uploaded {display_name} to corpus")
            uploaded.append(display_name)
        except Exception as e:
            print(f"Error uploading file {display_name}: {e}")
    return uploaded

def list_user_corpus_files():
    """
    Lists all files in the user's RAG corpus.
    """
    initialize_vertex_ai()
    corpus = create_or_get_corpus()
    files = list(rag.list_files(corpus_name=corpus.name))
    print(f"Total files in corpus: {len(files)}")
    for file in files:
        print(f"File: {file.display_name} - {file.name}")
    return [file.display_name for file in files] 