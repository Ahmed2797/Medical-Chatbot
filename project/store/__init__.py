from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List

class VectorStorePipeline:

    def __init__(self, persist_path: str = "faiss_index"):
        self.persist_path = persist_path

    def store(self, docs: List[Document], embedding):
        """
        Store documents into FAISS and save locally
        """
        vector_store = FAISS.from_documents(docs, embedding)
        vector_store.save_local(self.persist_path)

    def load_retriever(self, embedding, k: int = 3):
        """
        Load FAISS index and return retriever
        """
        vector_store = FAISS.load_local(
            self.persist_path,
            embedding,
            allow_dangerous_deserialization=True
        )
        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

    def search(self, retriever, query: str, k: int = 4):
        """
        Similarity search with score
        """
        return retriever.vectorstore.similarity_search_with_score(query, k=k)
