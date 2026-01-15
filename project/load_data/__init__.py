from langchain_community.document_loaders import PyPDFLoader 


class DocumentProcessor:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.loader = PyPDFLoader(self.file_path)
    
    def load_documents(self):
        documents = self.loader.load()
        return documents
    
    def display_pages(self,documents,idx=5,num_chars=200):
        for idx,page in enumerate(documents[:idx]):
            print(f"Page: {idx}")
            print("Page_content:",page.page_content[:num_chars])
        


if __name__ == "__main__":
    processor = DocumentProcessor("project/data/Medical_book.pdf")
    docs = processor.load_documents()
    processor.display_pages(docs,idx=5,num_chars=200)