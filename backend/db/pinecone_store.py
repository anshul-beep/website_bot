import pinecone
from pinecone import ServerlessSpec
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_core.documents import Document

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index_name = "web-scripts"

# Create the Pinecone index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Vertex AI Embeddings
embeddings = VertexAIEmbeddings(model="text-embedding-004")

# Initialize Vector Store
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

def clear_pinecone_index(namespace=None):

    try:
        index.delete(delete_all=True, namespace=namespace)
        print("Successfully cleared all old embeddings from Pinecone!")
    except Exception as e:
        print(f"Error clearing Pinecone index: {e}")



def save_documents_to_pinecone(docs):
    try:
        clear_pinecone_index()

        if isinstance(docs[0], str):
            docs = [Document(page_content=doc) for doc in docs]

        uuids = [str(uuid4()) for _ in range(len(docs))]
        vector_store.add_documents(documents=docs, ids=uuids)
        print(f"Successfully stored {len(docs)} documents in Pinecone!")
        return True  
    except Exception as e:
        print(f"Error storing documents in Pinecone: {e}")
        return False
