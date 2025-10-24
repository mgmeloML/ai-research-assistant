from fastapi import FastAPI, HTTPException
import os, glob
from datetime import datetime
from dotenv import load_dotenv
from rag_core.data_collection import collect_pdf_data, collect_web_data
from rag_core.load_and_clean import load_pdf_docs, load_scraped_docs
from rag_core.chunk_docs import split_text
from rag_core.build_index import make_database, get_embedding_function, retrieve_docs, delete_collection
from rag_core.generate import generate_response, generate_chat_name, generate_collection_name, num_sources
from models import Chat
from database import chat_collection
from serializers import chatSerializer

load_dotenv()

embeddings = get_embedding_function()
scraped_dir = os.getenv("SCRAPE_DIR")
pdf_dir = os.getenv("PDF_DIR")
vector_path = os.getenv("VECTOR_DIR")


app = FastAPI()

@app.post("/create_chat")
async def add_to_collection():
    chat = Chat()
    chat_dict = chat.model_dump()
    chat_dict["chat_id"] = str(chat.chat_id)
    chat_collection.insert_one(chat_dict)
    return {"status": "Successfully created a new chat"}

@app.get("/get_chats")
async def chat_list():
    chats = chat_collection.find({})
    serialized = [chatSerializer(chat) for chat in chats]
    return serialized

@app.get("/get_chat/{chat_id}")
async def get_chat(chat_id: str):
    chat = chat_collection.find_one({"chat_id": chat_id})
    return chat["chat_history"]

@app.delete("/delete_chat/{chat_id}")
async def delete_chat(chat_id: str):
    collection = chatSerializer(chat_collection.find_one({"chat_id": chat_id}))["collection_name"]
    print(collection)
    chat_collection.delete_one({"chat_id": chat_id})
    if collection:
        delete_collection(collection)
    return {"Satus": "Successfully deleted a chat"}

@app.post("/web_rag/{chat_id}")
async def web_rag(chat_id: str, query: str):
    chat = chat_collection.find_one({"chat_id": chat_id})

    chat_history = chat["chat_history"]
    collection_name = chat["collection_name"]
    chat_name = chat["chat_name"]

    if not chat_history:
        max_results = int(num_sources(query))
        collect_web_data(query=query, directory=scraped_dir, max_results=max_results)
        documents = load_scraped_docs(scraped_dir)
        chunks = split_text(documents=documents)
        if not collection_name:
            collection_name = generate_collection_name(query)
            chat_collection.update_one({"chat_id": chat_id}, {"$set": {"collection_name": collection_name}})
        if chat_name == "new chat":
            chat_name = generate_chat_name(query)
            chat_collection.update_one({"chat_id": chat_id}, {"$set": {"chat_name": chat_name}})
        make_database(chunks, collection_name=collection_name)

    single_vector = embeddings.embed_query(query)
    docs = retrieve_docs(single_vector, collection_name=collection_name)
    answer = generate_response(docs, query, history=chat_history)
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})

    chat_collection.update_one({"chat_id": chat_id}, {"$set": {"chat_history": chat_history}})
    chat_collection.update_one({"chat_id": chat_id}, {"$set": {"modified_at": datetime.now()}})
    [os.remove(f) for f in glob.glob(f"{scraped_dir}*") if os.path.isfile(f)]
    return {"respone": answer}

@app.post("/pdf_rag/{chat_id}")
async def pdf_rag(chat_id: str, query: str):
    chat = chat_collection.find_one({"chat_id": chat_id})

    chat_history = chat["chat_history"]
    collection_name = chat["collection_name"]
    chat_name = chat["chat_name"]

    if not chat_history:
        max_results = int(num_sources(query))
        collect_pdf_data(query=query, directory=pdf_dir, max_results=max_results)
        documents = load_pdf_docs(pdf_dir)
        chunks = split_text(documents=documents)
        if not collection_name:
            collection_name = generate_collection_name(query)
            chat_collection.update_one({"chat_id": chat_id}, {"$set": {"collection_name": collection_name}})
        if chat_name == "new chat":
            chat_name = generate_chat_name(query)
            chat_collection.update_one({"chat_id": chat_id}, {"$set": {"chat_name": chat_name}})
        make_database(chunks, collection_name=collection_name)

    single_vector = embeddings.embed_query(query)
    docs = retrieve_docs(single_vector, collection_name=collection_name)
    answer = generate_response(docs, query, history=chat_history)
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})

    chat_collection.update_one({"chat_id": chat_id}, {"$set": {"chat_history": chat_history}})
    chat_collection.update_one({"chat_id": chat_id}, {"$set": {"modified_at": datetime.now()}})
    [os.remove(f) for f in glob.glob(f"{pdf_dir}*") if os.path.isfile(f)]
    return {"respone": answer}