"""data_analyst_agent for finding information using google search"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

greeter_agent = Agent(
    model=MODEL,
    name="greeter_agent",
    instruction=prompt.GREETER_AGENT_PROMPT,
    output_key="greeter_agent_output",
    tools=[google_search],
)