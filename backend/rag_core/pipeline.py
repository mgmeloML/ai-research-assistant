import os, glob
from dotenv import load_dotenv
from rag_core.data_collection import collect_pdf_data, collect_web_data
from rag_core.load_and_clean import load_pdf_docs, load_scraped_docs
from rag_core.chunk_docs import split_text
from rag_core.build_index import make_database, get_embedding_function, retrieve_docs
from rag_core.generate import generate_response, generate_chat_name, generate_collection_name, num_sources


load_dotenv()

embeddings = get_embedding_function()
scraped_dir = os.getenv("SCRAPE_DIR")
pdf_dir = os.getenv("PDF_DIR")
vector_path = os.getenv("VECTOR_DIR")



def rag_pdf():
    query = str(input("your input:"))
    max_results = int(num_sources(query))
    collect_pdf_data(query=query, directory=pdf_dir, max_results=max_results)
    documents = load_pdf_docs(pdf_dir)
    chunks = split_text(documents=documents)
    single_vector = embeddings.embed_query(query)
    collection_name = generate_collection_name(query)
    make_database(chunks, collection_name=collection_name)
    docs = retrieve_docs(single_vector, collection_name=collection_name)
    generate_response(docs, query)

def rag_web():
    query = str(input("your input:"))
    max_results = int(num_sources(query))
    collect_web_data(query=query, directory=scraped_dir, max_results=max_results)
    documents = load_scraped_docs(scraped_dir)
    chunks = split_text(documents=documents)
    single_vector = embeddings.embed_query(query)
    collection_name = generate_collection_name(query)
    make_database(chunks, collection_name=collection_name)
    docs = retrieve_docs(single_vector, collection_name=collection_name)
    generate_response(docs, query)


flow = str(input("do you want web or pdf pipeline?:"))
if flow == "web":
    rag_web()
elif flow == "pdf":
    rag_pdf()

[os.remove(f) for f in glob.glob(f"{scraped_dir}*") if os.path.isfile(f)]
[os.remove(f) for f in glob.glob(f"{pdf_dir}*") if os.path.isfile(f)]