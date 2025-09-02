from langchain_community.document_loaders import PyPDFDirectoryLoader
import os
import re
from dotenv import load_dotenv

load_dotenv()

def clean_pdf_text(text):
    # Fix line breaks
    text = re.sub(r'-\s*\n\s*', '', text)  # fix hyphenation
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # join lines
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove page numbers
    text = re.sub(r'\n\d+\n', '\n', text)
    # Optional: remove references
    text = re.split(r'\nReferences\n', text, flags=re.IGNORECASE)[0]
    return text.strip()

dir_path = os.getenv("PDF_DIR")

loader = PyPDFDirectoryLoader(dir_path)
docs = loader.load()

print(len(docs[0].page_content))
for doc in docs:
    doc.page_content = clean_pdf_text(doc.page_content)

