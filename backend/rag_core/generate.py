from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


PROMPT_TEMPLATE = """
You are a research assistant. Answer the user's question using only the provided context. 
If the context does not contain enough information, say so honestly.

Context:
{context}

---

Question: {question}

Instructions:
- Write a detailed, well-structured answer (at least 3-5 paragraphs).  
- Use bullet points or paragraphs if needed for clarity.
"""

model = OllamaLLM(model="gemma3:4b")

def generate_response(docs, query):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs]) 
    prompt = prompt_template.format(context=context_text, question=query)

    response_text = model.invoke(prompt)
    sources = list(set([doc.metadata["source"] for doc in docs]))
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)