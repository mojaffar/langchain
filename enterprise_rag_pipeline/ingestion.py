from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_all_pdfs(data_dir):

    all_docs = []

    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):

            pdf_path = os.path.join(data_dir, file)

            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(all_docs)