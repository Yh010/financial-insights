"""Root agent"""
import os
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt
from .sub_agents.calculator_agent import calculator_agent
from .sub_agents.greeter_agent import greeter_agent
from .sub_agents.extractor_agent import extractor_agent
from .agents.corpus_uploader_agent import corpus_uploader_agent
from .agents.retriever_agent import retriever_agent
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

MODEL = "gemini-2.5-pro"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
location= "us-central1"
print(PROJECT_ID)
BUCKET_NAME = os.getenv("GOOGLE_CLOUD_BUCKET")
vertexai.init(project=PROJECT_ID, location=location,staging_bucket=BUCKET_NAME,api_key="")
#genai.Client(
 #       vertexai=True,
  #      project="deft-justice-466615-b0",
   #     location="global",
    #)

financial_coordinator = LlmAgent(
    name="financial_coordinator",
    model=MODEL,
    description=(
        "give appropriate response depending on the user's prompt"
    ),
    instruction=prompt.ROUTING_AGENT_PROMPT,
    output_key="financial_coordinator_output",
    tools=[
        AgentTool(agent=calculator_agent),
        AgentTool(agent=greeter_agent),
        AgentTool(agent=extractor_agent),
        AgentTool(agent=corpus_uploader_agent),
        AgentTool(agent=retriever_agent),
    ],
)

root_agent = financial_coordinator