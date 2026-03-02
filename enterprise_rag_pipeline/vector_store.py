from langchain_community.vectorstores import FAISS
from llm_config import embeddings

VECTOR_DB_PATH = "faiss_index"

def create_vector_store(chunks):

    vectorstore = FAISS.from_documents(
        chunks,
        embedding=embeddings
    )

    vectorstore.save_local(VECTOR_DB_PATH)

    return vectorstore


def load_vector_store():

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )