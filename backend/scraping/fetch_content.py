from langchain_text_splitters import RecursiveCharacterTextSplitter
from playwright.sync_api import sync_playwright

def fetch_and_split_website_content(url: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        
       
        page.goto(url)
        page.wait_for_selector("body")  
        content = page.inner_text("body")  
        browser.close()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(content)
    
    return chunks