from google.adk.agents import ParallelAgent
from app.agents.corpus_uploader_agent import corpus_uploader_agent
from app.agents.pass_generator_agent import pass_generator_agent


router_agent = ParallelAgent(
    name="router_agent",
    sub_agents=[corpus_uploader_agent, pass_generator_agent],    
)