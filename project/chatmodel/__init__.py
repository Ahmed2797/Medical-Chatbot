from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')


class Groqllm:
    def __init__(self, model="llama-3.1-8b-instant", api_key=None, max_tokens=500):
        self.model = model
        self.api_key = api_key
        self.max_tokens = max_tokens
    
    def call(self):

        model = ChatGroq(
            model=self.model,
            api_key=self.api_key,
            max_tokens=self.max_tokens
        )
        return model
    
    def invoke(self,query:str):
        llm = self.call()
        response = llm.invoke(query)

        return response
    

if __name__ == "__main__":
    llm = Groqllm(api_key=groq_api_key)
    model = llm.call()
    print(model.invoke("Hello, LangChain with Groq!"))
