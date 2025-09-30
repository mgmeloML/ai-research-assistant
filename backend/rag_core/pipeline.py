import os
from dotenv import load_dotenv
from rag_core.data_collection import collect_pdf_data, collect_web_data
from rag_core.load_and_clean import load_pdf_docs, load_scraped_docs
from rag_core.chunk_docs import split_text
from rag_core.build_index import make_database, get_embedding_function, retrieve_docs
from rag_core.generate import generate_response


load_dotenv()#

embeddings = get_embedding_function()
scraped_dir = os.getenv("SCRAPE_DIR")
pdf_dir = os.getenv("PDF_DIR")
vector_path = os.getenv("VECTOR_DIR")



def rag_pdf():
    query = str(input("your input:"))
    collect_pdf_data(query=query, directory=pdf_dir, max_results=5)
    documents = load_pdf_docs(pdf_dir)
    chunks = split_text(documents=documents)
    single_vector = embeddings.embed_query(query)

    make_database(chunks, collection_name="pdf")
    docs = retrieve_docs(single_vector, collection_name="pdf")
    generate_response(docs, query)

def rag_web():
    query = str(input("your input:"))
    collect_web_data(query=query, directory=scraped_dir, max_results=5)
    documents = load_scraped_docs(scraped_dir)
    chunks = split_text(documents=documents)
    single_vector = embeddings.embed_query(query)

    make_database(chunks, collection_name="web")
    docs = retrieve_docs(single_vector, collection_name="web")
    generate_response(docs, query)

flow = str(input("do you want web or pdf pipeline?:"))
if flow == "web":
    rag_web()
elif flow == "pdf":
    rag_pdf()