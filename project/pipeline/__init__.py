from project.chatmodel import Groqllm
from project.load_data import DocumentProcessor
from project.chunk import SplitterDocumentProcessor
from project.embed import EmbeddingPipeline
from project.store import VectorStorePipeline
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from project.prompt import template

from dotenv import load_dotenv
import os
import sys

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
pdf_path = "project/data/Medical_book.pdf"
persist_path="faiss_index"


# pipeline.py - SIMPLE VERSION
from dotenv import load_dotenv
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def main_pipeline():
    """
    Simple pipeline that loads pre-built vector store
    """
    print("🔧 Loading Medical Chatbot...")
    
    # 1. Get API key
    groq_api_key = os.getenv('GROQ_API_KEY')

    print("🔧 Loading Grpq LLM...")
    llm = Groqllm(api_key=groq_api_key)
    model = llm.call()

    # Load Data
    print("🔧 Loading Data...")
    processor = DocumentProcessor(file_path=pdf_path)
    documents = processor.load_documents()
    
    # 4. Load embedding model
    print("🔄 Loading embeddings...")
    em_pipe = EmbeddingPipeline(persist_path=persist_path)



## Firt time run code 
    ## em_pipe.create_vector_store(documents)
    


    # 5. Check if vector store exists
    print("🔄 Checking vector store...")
    if not os.path.exists(persist_path):
        print("❌ Vector store not found!")

    print("💡 Create Vector store sucessfull")
        

    # 6. Load retriever
    print("🔄 Loading vector store...")
    em_model = em_pipe.embed_model()
    retriever = em_pipe.load_retriever(em_model)
    
    # 7. Create chain
    print("🔄 Creating chain...")
    prompt = template()
    combine_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_chain)
    
    print("✅ Chatbot ready!")
    return retrieval_chain

if __name__ == "__main__":
    try:
        chain = main_pipeline()
        print("\n🧪 Testing...")
        response = chain.invoke({"input": "What is Abortion, therapeutic?"})
        print(f"🤖 {response['answer'][:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")