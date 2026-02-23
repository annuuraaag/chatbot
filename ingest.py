import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


DOCS_PATH = "docs"


def load_documents():
    documents = []

    for file in os.listdir(DOCS_PATH):
        path = os.path.join(DOCS_PATH, file)

        # -------- TXT --------
        if file.endswith(".txt"):
            loader = TextLoader(path)
            documents.extend(loader.load())

        # -------- PDF --------
        elif file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

    return documents


# Optional: Add web pages here
def load_web_docs():
    urls = [
        # Example:
        # "https://langchain.com"
    ]

    if not urls:
        return []

    loader = WebBaseLoader(urls)
    return loader.load()


# -------- Load all documents --------

documents = load_documents()
documents.extend(load_web_docs())

print(f"Loaded {len(documents)} documents")

# -------- Split into chunks --------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# -------- Create embeddings --------

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# -------- Build FAISS index --------

vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore.save_local("faiss_index")

print("✅ Universal knowledge base indexed successfully.")