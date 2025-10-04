from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


model = OllamaLLM(model="granite3.3:8b")

PROMPT_TEMPLATE = """
You are a research assistant. Use the conversation history and the provided context
to answer the user's question. If the context does not contain enough information,
say so honestly rather than making something up.

Conversation history:
{history}

Context:
{context}

---

User's current question:
{question}

Instructions:
- Write a detailed, well-structured answer (at least 3–5 paragraphs).
- Use bullet points or paragraphs if needed for clarity.
- Make sure the answer is grounded in the given context and consistent with the conversation history.
"""

COLLECTION_NAME_TEMPLATE = """
You are an assistant that generates a clean and consistent collection name for a ChromaDB database.

User Query: "{question}"

Guidelines:
- Summarize the user query into 2-5 descriptive words.
- Use only lowercase letters, numbers, and underscores.
- No special characters, spaces, or punctuation.
- Keep the name concise but meaningful.
- Avoid stopwords like "the", "a", "of", etc.
- If multiple queries are similar, generate deterministic names (same query → same name).

Return only the final collection name and nothing more.
"""

NUM_SOURCES_TEMPLATE = """
You are an assistant that decides how many sources should be retrieved from a vector database for a Retrieval-Augmented Generation (RAG) pipeline.

User Query: "{question}"

Guidelines:
- For simple factual or definition-style queries, choose a small number of sources (1-3).
- For moderately complex queries that need context or comparison, choose a medium number of sources (3-5).
- For broad, open-ended, or research-style queries, choose a larger number of sources (5-8).
- Always balance between precision (fewer, more relevant sources) and recall (more diverse sources).
- Return only an integer number of sources.

Return only a single integer and nothing more
"""

CHAT_NAME_TEMPLATE = """
You are an assistant that generates a short, descriptive, and memorable name for a chat based on the user's question.

User Question: "{question}"

Guidelines:
- Summarize the essence of the question in 3-6 words.
- Use lowercase letters, numbers and "-" only.
- No spaces, punctuation, or special characters.
- Avoid generic words like "chat", "discussion", "topic".
- Make it catchy and meaningful so someone can identify the chat at a glance.

Return only the final chat name and nothing more.
"""

def generate_chat_name(query):
    prompt_template = ChatPromptTemplate.from_template(CHAT_NAME_TEMPLATE)
    prompt = prompt_template.format(question=query)
    response = model.invoke(prompt)
    print(response)

def num_sources(query):
    prompt_template = ChatPromptTemplate.from_template(NUM_SOURCES_TEMPLATE)
    prompt = prompt_template.format(question=query)
    response = model.invoke(prompt)
    print(response)

def generate_collection_name(query):
    prompt_template = ChatPromptTemplate.from_template(COLLECTION_NAME_TEMPLATE)
    prompt = prompt_template.format(question=query)
    response = model.invoke(prompt)
    print(response)

def generate_response(docs, query, history = None):
    
    history_text = ""
    if history:
        for turn in history:
            history_text += f"{turn['role'].capitalize()}: {turn['content']}\n"
    else:
        history_text = "No prior conversation.\n"

    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs]) 

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query, history=history_text)

    response_text = model.invoke(prompt)
    sources = list(set([doc.metadata["source"] for doc in docs]))
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)

if __name__ == "__main__":
    question = "explain how A* search works and why the heuristic must be admissible"
    generate_chat_name(question)
    generate_collection_name(question)
    num_sources(question)