"""extractor_agent for extracting structured data from receipt images using Gemini and the extractor function."""

from google.adk import Agent
# No need for google_search tool here
from . import prompt
from app.agents.router_agent import router_agent

MODEL = "gemini-2.5-pro"

extractor_agent = Agent(
    model=MODEL,
    name="extractor_agent",
    description="Extracts structured data from receipt images and documents.",
    instruction=prompt.EXTRACTOR_AGENT_PROMPT,
    #output_key="extractor_agent_output",
    #tools=[],
    sub_agents=[router_agent]
)

# from google.adk import Agent
# from app.wallet_service.wallet_service import generate_wallet_pass_link
# from app.rag_test.prepare_corpus_and_data import upload_user_documents_to_corpus
# import json

# # Define the combined instruction prompt
# RECEIPT_PROCESSOR_PROMPT = """
# Role: You are an expert financial assistant specializing in receipt analysis.

# Workflow:
# 1.  First, analyze the user-provided receipt image(s) to understand their contents.
# 2.  Next, extract the financial details into a structured JSON object using the precise schema defined below.
# 3.  Finally, after you have successfully created the JSON output, you MUST perform two actions in parallel, in a single turn:
#     a. Call the `generate_wallet_pass_link` tool, passing the complete JSON object as the `receipt_data`.
#     b. Call the `upload_dict_as_text_to_corpus` tool, passing the complete JSON object as the `extracted_data`.

# JSON Schema:
# {
#   "merchant_name": "string",
#   "purchase_date": "YYYY-MM-DD",
#   "total_amount": "float",
#   "tax_amount": "float",
#   "items": [
#     {
#       "description": "string",
#       "quantity": "integer",
#       "price": "float"
#     }
#   ]
# }

# Rules:
# - If multiple images are provided, create an array of JSON objects.
# - If a value cannot be found for a field, use null.
# - Do not respond directly to the user with the JSON. Your final output must come from the tool calls.
# """

# # # New tool to handle the text conversion cleanly
# # def upload_dict_as_text_to_corpus(extracted_data: dict):
# #     """Converts a dictionary to a string and uploads it to the corpus."""
# #     # Convert the dictionary to a nicely formatted string
# #     text_to_upload = json.dumps(extracted_data, indent=2)
# #     return upload_extracted_text_to_corpus(text=text_to_upload)

# # Yash solution
# def upload_extracted_text_to_corpus(text: str, filename: Optional[str] = None):
#     # Save the extracted text to a temporary file
#     with tempfile.TemporaryDirectory() as temp_dir:
#         if not filename:
#             filename = "extracted_data.txt"
#         file_path = os.path.join(temp_dir, filename)
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(text)
#         uploaded = upload_user_documents_to_corpus([file_path])
#     return {"uploaded": uploaded}

# # The single, consolidated agent
# receipt_processor_agent = Agent(
#     model='gemini-2.5-pro',
#     name='receipt_processor_agent',
#     description="Extracts data from a receipt, generates a wallet pass, and archives the text.",
#     instruction=RECEIPT_PROCESSOR_PROMPT,
#     tools=[
#         generate_wallet_pass_link,
#         upload_dict_as_text_to_corpus # Use the new combined tool
#     ],
# )