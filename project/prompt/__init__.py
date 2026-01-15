from langchain_core.prompts import PromptTemplate

def template():
    """Return prompt template for chatbot"""
    prompt_template = """
    You are a helpful Medical AI assistant. Answer questions based on the provided context.
    
    CONTEXT:
    {context}
    
    QUESTION:
    {input}
    
    INSTRUCTIONS:
    1. Use only information from the context
    2. If context doesn't contain answer, say "I don't know"
    3. Keep answer concise (2-3 sentences)
    4. Use simple language
    
    ANSWER:
    """
    
    return PromptTemplate.from_template(prompt_template)

