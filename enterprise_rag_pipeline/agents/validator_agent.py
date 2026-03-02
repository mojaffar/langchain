def validator_agent(answer):

    unsafe_words = ["hack", "attack", "bomb"]

    for word in unsafe_words:
        if word in answer.lower():
            return "UNSAFE"

    return "SAFE"