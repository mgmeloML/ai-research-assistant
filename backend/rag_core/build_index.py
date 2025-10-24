from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def get_collection(collection_name: str):
    return Chroma(
        persist_directory="data/vector_store",
        embedding_function=get_embedding_function(),
        collection_name=collection_name
    )

def delete_collection(collection_name: str):
    store = Chroma(
        persist_directory="data/vector_store",
        collection_name=collection_name
    )
    client = store._client
    client.delete_collection(collection_name)

    
def make_database(chunks, collection_name):
    db = Chroma.from_documents(
        persist_directory="data/vector_store",
        embedding=get_embedding_function(),
        collection_name=collection_name,
        documents=chunks
    )

    return db

def retrieve_docs(query: str, collection_name: str, k: int = 5):
    db = get_collection(collection_name)
    results = db.similarity_search_by_vector(query, k=k) 
    return results