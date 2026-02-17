import streamlit as st
import os
import time
from dotenv import load_dotenv

from langchain_groq import ChatGroq
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

# Prompt Template
prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based only on the provided context.
    Provide the most accurate response.

    <context>
    {context}
    </context>

    Question: {input}
    """
)

# Function to create vector embeddings
def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        st.session_state.loader = PyPDFDirectoryLoader("research_papers")
        st.session_state.docs = st.session_state.loader.load()

        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        st.session_state.final_documents = (
            st.session_state.text_splitter.split_documents(
                st.session_state.docs[:50]
            )
        )

        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_documents,
            st.session_state.embeddings
        )

# Streamlit UI
st.title("RAG Document Q&A With Groq And Llama3")

user_prompt = st.text_input("Enter your query from the research paper")

if st.button("Document Embedding"):
    create_vector_embedding()
    st.success("Vector Database is ready")

# RAG Execution
if user_prompt and "vectors" in st.session_state:

    retriever = st.session_state.vectors.as_retriever()

    # Format retrieved docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Modern LCEL RAG pipeline
    rag_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    start = time.process_time()
    response = rag_chain.invoke(user_prompt)
    end = time.process_time()

    st.write("### Answer:")
    st.write(response)

    st.write(f"Response time: {end - start:.2f} seconds")

    # Show retrieved documents
    with st.expander("Document Similarity Search"):
        docs = retriever.invoke(user_prompt)
        for doc in docs:
            st.write(doc.page_content)
            st.write("---------------------------")
