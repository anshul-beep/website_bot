from langchain_text_splitters import RecursiveCharacterTextSplitter
from playwright.sync_api import sync_playwright

def fetch_and_split_website_content(url: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Fetches content from a dynamic website using Playwright, splits it into chunks, and returns the documents.

    Args:
        url (str): The website URL to scrape.
        chunk_size (int): The maximum size of each text chunk. Default is 1000.
        chunk_overlap (int): The overlap size between chunks. Default is 200.

    Returns:
        List[str]: A list of split text chunks.
    """
    # Use Playwright to fetch the page content
    with sync_playwright() as p:
        # Launch a browser instance
        browser = p.chromium.launch(headless=True)  # Set headless=False for debugging
        page = browser.new_page()
        
        # Navigate to the URL
        page.goto(url)
        
        # Wait for the content to load (adjust the selector as needed)
        page.wait_for_selector("body")  # Wait for the body to load
        
        # Extract the text content of the page
        content = page.inner_text("body")  # Extract all text from the body
        
        # Close the browser
        browser.close()

    # Split the content into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(content)
    
    return chunks