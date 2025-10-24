from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks