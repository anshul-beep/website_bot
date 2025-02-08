import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Embeddings & Chat App", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("Embeddings & Chat App")
st.markdown("This app allows you to store URL embeddings and ask questions about the stored content.")

# Input for URL
st.header("Step 1: Store URL Embeddings")
url = st.text_input("Enter the URL to store embeddings:", placeholder="https://example.com")

# Button to store embeddings
if st.button("Store Embeddings"):
    if url:
        # API call to store embeddings
        api_url = "http://127.0.0.1:5000/api/store-embeddings"
        payload = {"url": url}
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            st.success("Embeddings stored successfully!")
        else:
            st.error(f"Failed to store embeddings. Error: {response.text}")
    else:
        st.warning("Please enter a valid URL.")

# Input for query
st.header("Step 2: Ask a Question")
query = st.text_input("Enter your question:", placeholder="What is the content of the stored embeddings?")

# Button to send query
if st.button("Ask Question"):
    if query:
        api_url = "http://127.0.0.1:5000/api/chat"
        payload = {"question": query}
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            answer_part = response_data.get("answer", "No answer found.")
            think_part = response_data.get("think", "No thought process available.")
            
            # Display "think" section
            st.subheader("Thought Process:")
            st.write(think_part)

            # Display "answer" section
            st.subheader("Answer:")
            st.write(answer_part)
        else:
            st.error(f"Failed to get an answer. Error: {response.text}")
    else:
        st.warning("Please enter a valid question.")