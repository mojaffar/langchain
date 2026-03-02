from llm_config import llm
from vector_store import load_vector_store

def execution_agent(query, plan):

    if "retrieve" in plan:

        vectorstore = load_vector_store()

        docs = vectorstore.similarity_search(query, k=3)

        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
        Answer the question using ONLY the context below.

        Context:
        {context}

        Question:
        {query}

        If answer not found, say:
        "I don't know from the provided documents."
        """

        response = llm.invoke(prompt)

        return response.content

    else:
        response = llm.invoke(query)
        return response.content