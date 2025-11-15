from langchain_community.vectorstores import Qdrant
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import settings
from database.qdrant_db import get_qdrant_client

def get_rag_chain():
    """Initializes and returns the RAG chain."""
    
    # 1. Initialize Embeddings and Vector Store
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    qdrant_client = get_qdrant_client()
    
    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        embeddings=embeddings
    )
    retriever = vector_store.as_retriever()

    # 2. Define the Prompt Template
    template = """
    You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise.

    Context: {context}

    Question: {question}

    Helpful Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 3. Initialize the LLM
    llm = ChatAnthropic(
        model=settings.ANTHROPIC_MODEL,
        api_key=settings.ANTHROPIC_API_KEY,
        temperature=0.1
    )

    # 4. Build the RAG Chain using LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# Create a singleton instance of the chain
rag_chain = get_rag_chain()