def validator_agent(answer):

    blocked_words = [
        "password",
        "admin",
        "secret",
        "token"
    ]

    for word in blocked_words:
        if word in answer.lower():
            return "UNSAFE"

    return "SAFE"