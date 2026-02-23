import ollama
from vector_store import retrieve

def execution_agent(query, plan):

    context = ""

    if plan["retrieval"]:
        context = retrieve(query)

    prompt = f"""
    Use the context if available.

    Context:
    {context}

    Question:
    {query}
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]