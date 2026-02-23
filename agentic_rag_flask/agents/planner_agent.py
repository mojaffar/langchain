def planner_agent(query):

    retrieval_keywords = [
        "pdf","document","file",
        "based on","according"
    ]

    for word in retrieval_keywords:
        if word in query.lower():
            return {"retrieval": True}

    return {"retrieval": False}