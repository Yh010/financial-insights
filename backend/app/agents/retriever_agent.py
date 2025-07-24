import os
from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

load_dotenv()

RETRIEVER_AGENT_PROMPT = """
You are a Retrieval-Augmented Generation (RAG) assistant. Your job is to answer user questions using ONLY the information found in the provided document corpus. You do not have access to any external knowledge or the internet.

Instructions:
- Only answer direct questions from the user. Do not respond to greetings, chit-chat, or unrelated requests.
- Use the retrieval tool to search the corpus for relevant information to answer the user's question.
- If the answer is found in the corpus, provide a clear, concise, and accurate response based solely on the retrieved content.
- Always cite your sources at the end of your answer. Use the document title and section, or file name, as provided by the retrieval tool.
- If the answer cannot be found in the corpus, clearly state: "I could not find the answer to your question in the provided documents."
- Do not speculate, make up information, or use any knowledge outside the corpus.
- Do not reveal your internal reasoning or retrieval process—just provide the answer and citations.

Citation Format:
- List all sources used at the end of your answer under a heading like "Citations" or "References."
- If your answer is based on multiple sources, cite each one only once.
- Example:
Citations:
1) Alphabet_10K_2024_corpus.pdf, Section 2
2) User_Uploaded_Corpus.txt

If you are unsure or the information is not available, say so clearly.
"""

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS")
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

retriever_agent = Agent(
    model='gemini-2.5-pro',
    name='retriever_agent',
    instruction=RETRIEVER_AGENT_PROMPT,
    tools=[
        ask_vertex_retrieval,
    ]
) 