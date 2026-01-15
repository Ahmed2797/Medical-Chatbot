from project.chatmodel import Groqllm
from project.load_data import DocumentProcessor
from project.embed import EmbeddingPipeline

from dotenv import load_dotenv
import os
import sys


pdf_path = "project/data/Medical_book.pdf"
persist_path="faiss_index"

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

def faiss_store():

    # Load Data
    print("🔧 Loading Data...")
    processor = DocumentProcessor(file_path=pdf_path)
    documents = processor.load_documents()

    # 4. Load embedding model
    print("🔄 Loading embeddings...")
    em_pipe = EmbeddingPipeline(persist_path=persist_path)



    # Firt time run code 
    em_pipe.create_vector_store(documents)

    print("Faiss Store Completed")

    return None

if __name__ == "__main__":
    faiss_store()


