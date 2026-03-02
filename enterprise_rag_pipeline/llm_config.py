from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
import os

# ---------------- LLM ----------------

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# ---------------- EMBEDDINGS ----------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)