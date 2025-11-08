from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from vector_db import get_vector_store
import os

def get_rag_chain():
    """
    Initializes and returns a RAG chain.
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever()

    # Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

    # Define the prompt template
    template = """
    You are an expert kindergarten teacher assistant. Your goal is to help the user create lesson plans and activities.
    Answer the user's question based only on the context provided.
    If you don't know the answer, just say that you don't know, don't try to make something up.

    Context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Create the RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
