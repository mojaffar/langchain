from llm_config import llm

def planner_agent(query):

    prompt = f"""
    Decide how to answer the query.

    Query: {query}

    If it requires document retrieval return: retrieve
    If it is general knowledge return: general

    Only return one word.
    """

    response = llm.invoke(prompt)

    return response.content.strip().lower()