from typing import List, Any

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from sentence_transformers import SentenceTransformer
from project.load_data import DocumentProcessor


class EmbeddingPipeline:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-l6-v2",
        chunk_size: int = 2000,
        chunk_overlap: int = 200,
        persist_path: str = "faiss_index"
    ):
        # SentenceTransformer (manual embedding if needed)
        self.model = SentenceTransformer(model_name)

        # LangChain-compatible embedding model
        self.hf_model = HuggingFaceEmbeddings(model_name=model_name)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_path = persist_path

    # --------------------------------------------------
    # Document Splitting
    # --------------------------------------------------
    def split_doc(self, documents: List[Any]) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        split_docs: List[Document] = []

        for doc in documents:
            chunks = text_splitter.split_text(doc.page_content)

            for chunk in chunks:
                split_docs.append(
                    Document(page_content=chunk)
                )

        return split_docs

    # --------------------------------------------------
    # Manual Embedding (SentenceTransformer)
    # --------------------------------------------------
    def embed_chunk(self, texts: List[Any]):
        if texts and hasattr(texts[0], "page_content"):
            text_contents = [doc.page_content for doc in texts]
        else:
            text_contents = texts

        embeddings = self.model.encode(
            text_contents,
            show_progress_bar=True
        )
        return embeddings

    # --------------------------------------------------
    # Return LangChain Embedding Model
    # --------------------------------------------------
    def embed_model(self):
        return self.hf_model

    # --------------------------------------------------
    # Create FAISS Vector Store
    # --------------------------------------------------
    def create_vector_store(
        self,
        documents: List[Document],
        persist_path: str | None = None
    ):
        split_docs = self.split_doc(documents)

        vector_store = FAISS.from_documents(
            split_docs,
            self.hf_model
        )

        if persist_path:
            vector_store.save_local(persist_path)
        else:
            vector_store.save_local(self.persist_path)

        return vector_store

    # --------------------------------------------------
    # Load Retriever
    # --------------------------------------------------
    def load_retriever(self, embedding, k: int = 3):
        vector_store = FAISS.load_local(
            self.persist_path,
            embedding,
            allow_dangerous_deserialization=True
        )

        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )


# --------------------------------------------------
# Example Usage
# --------------------------------------------------
if __name__ == "__main__":
    loader = DocumentProcessor("project/data/Medical_book.pdf")
    docs = loader.load_documents()

    emb_pipe = EmbeddingPipeline()
    texts = emb_pipe.split_doc(docs)

    print(f"Split into {len(texts)} chunks")
