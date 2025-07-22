"""data_analyst_agent for finding information using google search"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

calculator_agent = Agent(
    model=MODEL,
    name="calculator_agent",
    instruction=prompt.calculator_agent_prompt,
    output_key="calculator_agent_output",
    tools=[google_search],
)