from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from project.load_data import DocumentProcessor


class SplitterDocumentProcessor:
    def __init__(self,documents,chunk_size=2000,chunk_overlap=200):
        self.documents = documents
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def split_doc(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        tests = []
        for doc in self.documents:
            #print("Original document length:", len(doc.page_content))
            chunks = text_splitter.split_text(doc.page_content)

            for idx,chunk in enumerate(chunks):
                #print(f"Chunk {idx} length:", len(chunk))
                chunk_doc = Document(page_content=chunk)
                tests.append(chunk_doc)
        
        return tests
    

if __name__ == '__main__':
    processor = DocumentProcessor("project/data/Medical_book.pdf")
    docs = processor.load_documents()
    split = SplitterDocumentProcessor(documents=docs, chunk_size=1000, chunk_overlap=200)
    texts = split.split_doc()