import re, json, requests, os
from app.agent import root_agent
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from app.functions.gemini import generate
from app.functions.extractor import extract
from google.oauth2 import service_account
from google.auth import transport
from fastapi import HTTPException
from dotenv import load_dotenv
from app.wallet_service.wallet_service import generate_wallet_pass_link
from pydantic import BaseModel, Field
from app.rag_test.prepare_corpus_and_data import upload_user_documents_to_corpus
#from app.rag_test.agent import router as rag_test_router
from google.adk.runners import Runner
import logging
from google.genai import types
from google.adk.sessions import InMemorySessionService
import uuid
from datetime import datetime

# Initialize session service
session_service = InMemorySessionService()

logger = logging.getLogger(__name__)

app = FastAPI()

load_dotenv(dotenv_path="app/.env")
ISSUER_ID = os.getenv("WALLET_ISSUER_ID")
#GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
#ISSUER_ID = "3388000000022967770"
print(ISSUER_ID)
#print(GOOGLE_CLOUD_PROJECT)
SERVICE_ACCOUNT_FILE = "app/jwt/rasheed-466715-3cf75e00c9e8.json"
PASS_CLASS_SUFFIX = "receipt_pass_class"

def generate_session_id(user_id: str) -> str:
    """Generate a unique session ID using UUID and timestamp."""
    return f"session_{user_id}_{datetime.utcnow():%Y%m%d%H%M%S}_{uuid.uuid4().hex[:6]}"

class ReceiptData(BaseModel):
    merchant_name: str
    purchase_date: str
    total_amount: float
    tax_amount: float
    items: list

class AgentQueryRequest(BaseModel):
    query: str

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
    uploaded = upload_user_documents_to_corpus(files)
    return {"uploaded": uploaded} 

#app.include_router(rag_test_router) 
@app.post("/run")
async def run(request_body: AgentQueryRequest):
    user_query = request_body.query
    user_id = "user"  # Replace with real user/session logic as needed
    session_id = generate_session_id(user_id)

    runner = Runner(
        app_name=app,
        agent=root_agent,
        session_service=session_service,  # Uncomment if you have session service
    )

    user_message = types.Content(
        role="user", parts=[types.Part.from_text(text=user_query)]
    )

    final_response_text = "No response from the Agent"
    last_event_content = None

    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    )

    async for event in events:
        logger.info(f"Received event from ADK: {event.author} ")
        if event.is_final_response():
            if event.content and event.content.parts:
                last_event_content = event.content.parts[0].text

    if last_event_content:
        final_response_text = last_event_content  # Or clean_html_response(last_event_content) if you have such a function
    else:
        logger.error("No final response event found from the Sequential Agent.")

    return {"response": final_response_text}

class AgentResponse(BaseModel):
    status: str
    response_text: str

@app.post("/agent-format", response_model=AgentResponse)
async def agent_format_endpoint(request_body: AgentQueryRequest):
    """
    Endpoint to interact with the agent using Runner, returning a structured response.
    """
    user_id = "user"  # Replace with real user/session logic as needed
    session_id = generate_session_id(user_id)
    user_query = request_body.query

    # Debug logging
    logger.info(f"Starting agent request - User: {user_id}, Session: {session_id}")
    logger.info(f"User query: {user_query}")
    logger.info(f"Project ID: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    logger.info(f"Model: gemini-2.5-pro")

    try:
        # Create session if it doesn't exist
        try:
            current_session = await session_service.get_session(
                app_name="FinancialApp",
                user_id=user_id,
                session_id=session_id,
            )
        except Exception as e:
            logger.warning(f"Session retrieval failed: {e}")
            current_session = None

        if current_session is None:
            current_session = await session_service.create_session(
                app_name="FinancialApp",
                user_id=user_id,
                session_id=session_id,
            )
            logger.info(f"Created new session: {session_id}")
        else:
            logger.info(f"Using existing session: {session_id}")

        runner = Runner(
            app_name="FinancialApp",
            agent=root_agent,
            session_service=session_service,
        )

        user_message = types.Content(
            role="user", parts=[types.Part.from_text(text=user_query)]
        )

        final_response_text = "No response from the Agent"
        last_event_content = None

        logger.info("Starting agent execution...")
        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
        )

        async for event in events:
            logger.info(f"Received event from ADK: {event.author} ")
            if event.is_final_response():
                if event.content and event.content.parts:
                    last_event_content = event.content.parts[0].text

        if last_event_content:
            final_response_text = last_event_content
        else:
            logger.error("No final response event found from the Agent.")

        return AgentResponse(status="success", response_text=final_response_text)

    except Exception as e:
        logger.error(f"Error querying agent: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process agent query: {e}")

@app.get("/test-gemini")
async def test_gemini():
    """
    Simple test endpoint to check if Gemini API is working.
    """
    try:
        from google.genai import GenerativeModel
        
        model = GenerativeModel("gemini-2.5-pro")
        response = model.generate_content("Hello, this is a test message.")
        
        return {
            "status": "success",
            "response": response.text,
            "model": "gemini-2.5-pro"
        }
    except Exception as e:
        logger.error(f"Gemini test failed: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "model": "gemini-2.5-pro"
        }
