from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_db = None

def create_vector_store(chunks):
    global vector_db
    vector_db = FAISS.from_documents(chunks, embedding_model)

def retrieve(query, k=3):
    docs = vector_db.similarity_search(query, k=k)
    return "\n".join([d.page_content for d in docs])