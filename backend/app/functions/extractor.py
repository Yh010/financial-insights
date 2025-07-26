from google import genai
from google.genai import types
import base64
from typing import List, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

def extract(image_bytes_list: Optional[List[bytes]] = None) -> str:
    """
    Generate a response from the Gemini model given a user prompt and optional images.
    Args:
        user_prompt (str): The user's input prompt.
        image_bytes_list (List[bytes], optional): List of image bytes to send to Gemini.
    Returns:
        str: The generated response from the Gemini model.
    """

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )
    user_prompt="""
    You are an expert financial assistant specializing in receipt analysis.
    Analyze the given receipt image and extract the following information.
    Return the output ONLY as a valid JSON object with the specified schema.
    If multiple images are uploaded, please return an array of json data
    If a value is not found, use null.


    JSON Schema:
    {
    "merchant_name": "string",
    "purchase_date": "YYYY-MM-DD",
    "total_amount": "float",
    "tax_amount": "float",
    "items": [
        {
        "description": "string",
        "quantity": "integer",
        "price": "float"
        }
    ]
    }
    If multiple images are uploaded, please return an array of json data
    If a value is not found, use null.

    """

    model = "gemini-2.5-flash-lite"
    parts = [types.Part.from_text(text=user_prompt)]
    if image_bytes_list:
        for img_bytes in image_bytes_list:
            parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))

    contents = [
        types.Content(
            role="user",
            parts=parts
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=65535,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text

    #json_string = response.text.strip().replace("json", "").replace("", "")
        
    #print("Successfully extracted data.")
    #return json.loads(json_string)
    return response