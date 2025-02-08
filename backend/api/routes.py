from flask import Blueprint, request, jsonify
from scraping.fetch_content import fetch_and_split_website_content
from db.pinecone_store import save_documents_to_pinecone
from generator.chatbot import graph
import re

api_bp = Blueprint('api', __name__)

@api_bp.route('/store-embeddings', methods=['POST'])
def store_embeddings():
    try:
        # Parse input data
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Invalid JSON or missing 'url'"}), 400

        url = data["url"]
        print(f"Processing URL: {url}")

        # Fetch and process website content
        try:
            all_splits = fetch_and_split_website_content(url)
            print(f"Fetched and split content into {len(all_splits)} documents.")
        except Exception as e:
            print(f"Error fetching and splitting content: {e}")
            return jsonify({"error": "Failed to fetch and process content."}), 500

        # Save embeddings to Pinecone
        try:
            success = save_documents_to_pinecone(all_splits)
            if success:
                return jsonify({"message": f"Embeddings for {len(all_splits)} documents stored successfully!"}), 200
            else:
                return jsonify({"error": "Failed to store embeddings."}), 500
        except Exception as e:
            print(f"Error storing embeddings: {e}")
            return jsonify({"error": "Failed to store embeddings."}), 500

    except Exception as e:
        print(f"Unexpected error in /store-embeddings: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@api_bp.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to retrieve context from Pinecone and generate answers using ChatGroq.
    """
    try:
        # Parse input data
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Invalid JSON or missing 'question'"}), 400

        question = data["question"]
        print(f"Processing question: {question}")

        # Initialize chatbot state
        state = {"question": question, "context": [], "answer": ""}

        # Run the chatbot graph
        try:
            result = graph.invoke(state)
            response=result["answer"]
            print(response)
            think_match = re.search(r"<think>(.*?)</think>", response, flags=re.DOTALL)
            think_part = think_match.group(1).strip() if think_match else "my name is anshul"

            final_answer = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
            return jsonify({"answer": final_answer, "think":think_part}), 200
        except Exception as e:
            print(f"Error running chatbot graph: {e}")
            return jsonify({"error": "Failed to generate response."}), 500

    except Exception as e:
        print(f"Unexpected error in /chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

