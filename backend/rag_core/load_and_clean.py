from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader
import os,re, json, html
from dotenv import load_dotenv

load_dotenv()

directory = os.getenv("PDF_DIR")
folder = os.getenv("SCRAPE_DIR")

def clean_pdf_text(text):
    text = re.sub(r'-\s*\n\s*', '', text) 
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text) 
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\d+\n', '\n', text)
    text = re.split(r'\nReferences\n', text, flags=re.IGNORECASE)[0]
    return text.strip()

def clean_scraped_text(text):
    text = re.sub(r"\[\d+\]", "", text)  
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\([^)]*adsbygoogle[^)]*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\([^)]*click here[^)]*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\([^)]*read more[^)]*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def resolve_metadata(doc , directory):
    meta = doc.metadata["source"]
    meta = meta.split("\\")[-1]
    meta = meta[:-4]

    with open(directory+"/"+meta+".json", "r") as f:
        metadata = json.load(f)

    title = metadata["title"]
    url = metadata["url"]
    doc.metadata["source"] = url
    doc.metadata["title"] = title
    
    return doc


def load_pdf_docs(directory):
    loader = PyPDFDirectoryLoader(directory)
    docs = loader.load()

    for doc in docs:
        doc.page_content = clean_pdf_text(doc.page_content)
        doc = resolve_metadata(doc=doc, directory=directory)

    return docs

def load_scraped_docs(directory):
    text_loader_kwargs = {"autodetect_encoding": True}
    loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader, silent_errors=True, loader_kwargs = text_loader_kwargs)
    docs = loader.load()

    for doc in docs:
        doc.page_content = clean_scraped_text(doc.page_content)
        doc = resolve_metadata(doc=doc, directory=directory)

    return docs

if __name__ == "__main__":
    print(load_pdf_docs(directory)[2])
