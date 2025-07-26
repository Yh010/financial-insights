import re, json, requests, os
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from app.functions.gemini import generate
from app.functions.extractor import extract
from app.functions.audio_processor import process_audio_receipt, transcribe_audio
from google.oauth2 import service_account
from google.auth import transport
from fastapi import HTTPException
from dotenv import load_dotenv
from app.wallet_service.wallet_service import generate_wallet_pass_link
from pydantic import BaseModel, Field
from app.rag_test.prepare_corpus_and_data import upload_user_documents_to_corpus
from app.api import chat
from fastapi.middleware.cors import CORSMiddleware
#from app.rag_test.agent import router as rag_test_router

app = FastAPI()

load_dotenv(dotenv_path="app/.env")
ISSUER_ID = os.getenv("WALLET_ISSUER_ID")
#GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
#ISSUER_ID = "3388000000022967770"
print(ISSUER_ID)
#print(GOOGLE_CLOUD_PROJECT)
SERVICE_ACCOUNT_FILE = "app/jwt/rasheed-466715-3cf75e00c9e8.json"
PASS_CLASS_SUFFIX = "receipt_pass_class"

origins = [
    "http://localhost",         # For local development
    "http://localhost:3000",    # For local React development
    "http://localhost:5173",    # For local Vite/React development
    "https://your-deployed-frontend-url.com", # Your production frontend
    "*"                         # A wildcard for open access (use with caution)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

app.include_router(chat.router, prefix="/api", tags=["Agent"])

class ReceiptData(BaseModel):
    merchant_name: str
    purchase_date: str
    total_amount: float
    tax_amount: float
    items: list

def get_gcp_access_token():
    """ Gets a short-lived access token for server-to-server calls."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/wallet_object.issuer"],
    )
    creds.refresh(transport.requests.Request())
    return creds.token

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

@app.post("/setup/create-wallet-class", tags=["setup"])
async def create_wallet_class():
    """ 
    A one-time utility endpoint to create a Google Wallet Pass Class..
    """

    token = get_gcp_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    class_payload = {
        "id": f"{ISSUER_ID}.{PASS_CLASS_SUFFIX}",
        "logo": {
            "sourceUri": {
                "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
            }
        },
        "classTemplateInfo": {
            "cardTemplateOverride": {
                "cardRowTemplateInfos": [
                    {
                        "twoItems": {
                            "startItem": {
                                "firstValue": {
                                    "fields": [
                                        {
                                            "fieldPath": "object.header"
                                        }
                                    ]
                                }
                            },
                            "endItem": {
                                "firstValue": {
                                    "fields": [
                                        {
                                            "fieldPath": "object.textModulesData['total']"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            },
            "detailsTemplateOverride": {
                "detailsItemInfos": [
                    {
                        "item": {
                            "firstValue": {
                                "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['purchase_date']"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "item": {
                            "firstValue": {
                                "fields": [
                                    {
                                        "fieldPath": "object.textModulesData['items_list']"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "item": {
                           "firstValue": {
                               "fields": [
                                   {
                                       "fieldPath": "object.linksModuleData.uris[0]"
                                   }
                               ]
                           }
                        }
                    }
                ]
            }
        }
    }
    
    url = "https://walletobjects.googleapis.com/walletobjects/v1/genericClass"
    
    print("Attempting to create a new Wallet Class...")
    response = requests.post(url, headers=headers, json=class_payload)
    
    if response.status_code == 200:
        print("✅ Class created successfully!")
        return response.json()
    elif response.status_code == 409:
        print("ℹ️ Class already exists.")
        return response.json()
    else:
        print(f"❌ Error creating class: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.json())


@app.post("/tools/create-receipt-pass", tags=["Agent Tools"])
async def tool_create_receipt_pass(receipt_data: ReceiptData):
    """
    An agent tool that generates a Google Wallet pass from receipt data.
    """
    # The Pydantic model automatically converts the incoming JSON to a dict
    receipt_dict = receipt_data.dict()
    
    save_url = generate_wallet_pass_link(receipt_dict)
    
    if not save_url:
        raise HTTPException(status_code=500, detail="Failed to generate Google Wallet pass link.")
    
    # The agent will receive this URL and can present it to the user.
    return {"wallet_save_url": save_url}

@app.post("/rag/upload")
def rag_upload(files: List[UploadFile] = File(...)):
    uploaded = upload_files_to_rag_corpus(files)
    return {"uploaded": uploaded} 

@app.post("/audio/transcribe")
async def transcribe_audio_endpoint(
    audio_file: UploadFile = File(...),
    language_code: str = Form("en-US")
):
    """
    Transcribe audio to text using Google Cloud Speech-to-Text.
    
    Args:
        audio_file: Audio file (mp3, wav, m4a, etc.)
        language_code: Language code for transcription (default: en-US)
    
    Returns:
        dict: Transcribed text
    """
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read audio file
        audio_bytes = await audio_file.read()
        
        # Transcribe audio
        transcript = transcribe_audio(audio_bytes, language_code, audio_file.filename)
        
        return {
            "status": "success",
            "transcript": transcript,
            "language_code": language_code
        }
        
    except Exception as e:
        print(f"Error in audio transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/audio/process-receipt")
async def process_audio_receipt_endpoint(
    audio_file: UploadFile = File(...),
    language_code: str = Form("en-US")
):
    """
    Process audio receipt: convert to text and extract receipt information.
    
    Args:
        audio_file: Audio file containing receipt information
        language_code: Language code for transcription (default: en-US)
    
    Returns:
        dict: Extracted receipt information
    """
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read audio file
        audio_bytes = await audio_file.read()
        
        # Process audio receipt
        receipt_data = process_audio_receipt(audio_bytes, language_code, audio_file.filename)
        
        return {
            "status": "success",
            "receipt_data": receipt_data,
            "language_code": language_code
        }
        
    except Exception as e:
        print(f"Error in audio receipt processing: {e}")
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

@app.post("/audio/create-pass-from-audio")
async def create_pass_from_audio_endpoint(
    audio_file: UploadFile = File(...),
    language_code: str = Form("en-US")
):
    """
    Complete pipeline: audio → text → receipt extraction → wallet pass creation.
    
    Args:
        audio_file: Audio file containing receipt information
        language_code: Language code for transcription (default: en-US)
    
    Returns:
        dict: Wallet pass URL
    """
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read audio file
        audio_bytes = await audio_file.read()
        
        # Process audio receipt
        receipt_data_str = process_audio_receipt(audio_bytes, language_code, audio_file.filename)
        
        # Parse the JSON response from Gemini
        import json
        try:
            # Clean up the response (remove markdown formatting if present)
            cleaned_response = receipt_data_str.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            receipt_data = json.loads(cleaned_response.strip())
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse receipt data: {str(e)}")
        
        # Create wallet pass
        save_url = generate_wallet_pass_link(receipt_data)
        
        if not save_url:
            raise HTTPException(status_code=500, detail="Failed to generate Google Wallet pass link.")
        
        return {
            "status": "success",
            "wallet_save_url": save_url,
            "receipt_data": receipt_data,
            "transcript": receipt_data_str
        }
        
    except Exception as e:
        print(f"Error in audio pass creation: {e}")
        raise HTTPException(status_code=500, detail=f"Audio pass creation failed: {str(e)}")

#app.include_router(rag_test_router) 
