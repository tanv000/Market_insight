from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def process_urls(urls):
    """
    Loads, splits, embeds, and indexes the given URLs.
    Returns: (FAISS vectorstore, raw documents)
    """
    loader = UnstructuredURLLoader(urls=urls)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs_split = splitter.split_documents(raw_docs)

    # Add source metadata for each chunk
    for i, doc in enumerate(docs_split):
        doc.metadata["source"] = urls[i % len(urls)]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs_split, embeddings)

    return vectorstore, raw_docs
