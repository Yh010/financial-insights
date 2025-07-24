from google.adk import Agent
from app.sub_agents.extractor_agent import extractor_agent

# This agent simply wraps the existing extractor_agent for modularity
# It can be used as a tool by other agents
image_extractor_agent = extractor_agent 