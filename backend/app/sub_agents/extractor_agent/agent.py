"""extractor_agent for extracting structured data from receipt images using Gemini and the extractor function."""

from google.adk import Agent
# No need for google_search tool here
from . import prompt

MODEL = "gemini-2.5-pro"

extractor_agent = Agent(
    model=MODEL,
    name="extractor_agent",
    description="Extracts structured data from receipt images and documents.",
    instruction=prompt.EXTRACTOR_AGENT_PROMPT,
    output_key="extractor_agent_output",
    tools=[],  # No external tools, extraction is handled by the agent logic
)