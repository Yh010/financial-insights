from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
#from ..dependencies import get_current_user  # Assuming this is in app/dependencies.py
from ..agent import root_agent  # Import your main agent from app/agent.py
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from pydantic import BaseModel

# --- Pydantic Models for Request/Response ---
class ChatResponse(BaseModel):
    status: str
    response_text: str
    session_id: str

# --- API Router ---
router = APIRouter()
APP_NAME = "FinancialInsights"

# Create a single, in-memory session service instance for the entire application.
session_service = InMemorySessionService()

APP_NAME = "Rasheed"
DEMO_USER_ID = "123456789012"
DEMO_SESSION_ID = "123456"



@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    #decoded_token: dict = Depends(get_current_user),
    query: Optional[str] = Form(""),
    #session_id: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    audio_files: Optional[List[UploadFile]] = File(None),
):
    """
    Handles a stateful, multimodal chat conversation with the root_agent.
    """
    #user_id = str(decoded_token.get("uid"))
    #active_session_id = session_id or user_id  # Use provided session_id or default to user_id

    # 1. --- Get or Create Session ---
    # try:
    #     current_session = await session_service.get_session(
    #         app_name=APP_NAME, user_id=user_id, session_id=active_session_id
    #     )
    #     if not current_session:
    #         current_session = await session_service.create_session(
    #             app_name=APP_NAME, user_id=user_id, session_id=active_session_id
    #         )
    #         print(f"Created new in-memory session: {active_session_id}")
    #     else:
    #         print(f"Resumed in-memory session: {active_session_id}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Session management error: {e}")

    try:
        current_session = await session_service.get_session(
            app_name=APP_NAME, user_id=DEMO_USER_ID, session_id=DEMO_SESSION_ID
        )
        if not current_session:
            current_session = await session_service.create_session(
                app_name=APP_NAME, user_id=DEMO_USER_ID, session_id=DEMO_SESSION_ID
            )
            print(f"Created new demo session: {DEMO_SESSION_ID}")
        else:
            print(f"Resumed demo session: {DEMO_SESSION_ID}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session management error: {e}")

    # 2. --- Initialize the ADK Runner ---
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # 3. --- Construct the Multimodal Message ---
    # message_parts = [types.Part.from_text(text=query)]
    # if images:
    #     for image in images:
    #         image_bytes = await image.read()
    #         message_parts.append(types.Part.from_bytes(data=image_bytes, mime_type=image.content_type))
    
    # user_message = types.Content(role="user", parts=message_parts)

    final_query = query
    
    # Process audio files first if present
    if audio_files:
        from ..functions.audio_processor import transcribe_audio
        audio_transcripts = []
        for audio_file in audio_files:
            if not audio_file.content_type.startswith('audio/'):
                raise HTTPException(status_code=400, detail="Audio file must be an audio file")
            
            audio_bytes = await audio_file.read()
            transcript = transcribe_audio(audio_bytes, filename=audio_file.filename)
            audio_transcripts.append(transcript)
        
        # Combine audio transcripts with the query
        if audio_transcripts:
            audio_text = " ".join(audio_transcripts)
            final_query = f"{final_query} {audio_text}".strip()
    
    # If there's an image but no text query, add a default one.
    if images and not final_query:
        final_query = "Analyze the attached image."
    
    # If there's audio but no text query, add a default one.
    if audio_files and not final_query:
        final_query = "Process the attached audio."

    message_parts = [types.Part.from_text(text=final_query)]
    if images:
        for image in images:
            image_bytes = await image.read()
            message_parts.append(types.Part.from_bytes(data=image_bytes, mime_type=image.content_type))
            
    if not final_query and not images and not audio_files:
        raise HTTPException(status_code=400, detail="Please provide a query, image, or audio file.")

    user_message = types.Content(role="user", parts=message_parts)

    print(user_message)
    # 4. --- Run the Agent and Get Response ---
    final_response = "Sorry, I encountered an issue. Please try again."
    try:
        events = runner.run_async(
            user_id=DEMO_USER_ID,
            session_id=DEMO_SESSION_ID,
            new_message=user_message,
        )

        async for event in events:
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {e}")

    return ChatResponse(
        status="success",
        response_text=final_response,
        session_id=DEMO_SESSION_ID
    )