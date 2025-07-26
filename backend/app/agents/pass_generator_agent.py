from google.adk import Agent
from app.wallet_service.wallet_service import generate_wallet_pass_link

PASS_GENERATOR_AGENT_PROMPT = """
You are a Google Wallet Pass Generator Agent. Your job is to generate a Google Wallet Pass for a given receipt.

Instructions:
- Use the data provided by the financial_coordinator to generate a Google Wallet Pass.
- If the data is not in JSON format, convert it to JSON format.
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
- Use the generate_wallet_pass_link tool to generate a Google Wallet Pass for the receipt.
- Return the Google Wallet Pass in the following format:
  {
    "pass_url": "https://wallet.google.com/pass/v1/passes/YOUR_PASS_ID/activate"
  }
- Whenever a pass is generated, return the pass_url.
- If the pass is not generated, return the error message from the generate_wallet_pass_link tool.

Do not modify the input data. Call the tool directly with the provided data.
"""

pass_generator_agent = Agent(
    model='gemini-2.5-pro',
    name='pass_generator_agent',
    description="Creates a Google Wallet Pass for a given receipt, and returns the pass_url string.",
    instruction=PASS_GENERATOR_AGENT_PROMPT,
    output_key="pass_generator_agent_output",
    tools=[generate_wallet_pass_link],
)
