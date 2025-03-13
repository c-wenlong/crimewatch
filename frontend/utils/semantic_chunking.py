from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_API = os.getenv("OPENAI_API")

def process_text_and_chunk(text: str):
    """
    Processes a plain text string and performs semantic chunking using LangChain's SemanticChunker.
    """
    try:
        semantic_chunker = SemanticChunker(OpenAIEmbeddings(api_key=OPENAI_API))
        
        docs = semantic_chunker.create_documents([text])

        print("Total number of chunks:", len(docs))
        
        chunk_texts = []
        for doc in docs:
            chunk_texts.append(doc.page_content)
        
        return chunk_texts
    except Exception as e:
        print(f"Error during text chunking: {e}")
        return None