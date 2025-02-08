import os
from langchain_groq import ChatGroq
import pinecone
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain import hub
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from dotenv import load_dotenv
import pinecone
import google.generativeai as genai
from langchain_google_vertexai import VertexAIEmbeddings
import re

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY )
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

index_name = "web-scripts"

index = pc.Index(index_name)
genai.configure(api_key=GEMINI_API_KEY)
embeddings = VertexAIEmbeddings(model="text-embedding-004")
vector_store = PineconeVectorStore(embedding=embeddings,index=index)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    """
    Retrieve relevant documents from the Pinecone vector store.
    """
    question = state["question"]
    retrieved_docs = vector_store.similarity_search(question)  
    return {"context": retrieved_docs}

def generate(state: State):
    """
    Generate an answer using ChatGroq and the retrieved context.
    """
    # Concatenate the content of retrieved documents
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])

    # Prepare the input for the prompt
    messages = prompt.invoke({"question": state["question"], "context": docs_content})

    # Generate a response using the ChatGroq model
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


