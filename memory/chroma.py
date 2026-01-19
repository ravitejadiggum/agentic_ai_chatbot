from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

def load_vectorstore():
    with open("data/documents.txt") as f:
        docs = [Document(page_content=line) for line in f.readlines()]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma.from_documents(
        docs, embeddings, persist_directory="./chroma_db"
    )
