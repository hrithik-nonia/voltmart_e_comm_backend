def plural_to_singular(word: str) -> str:
    word = word.strip()

    if word.endswith("ies"):
        return word[:-3] + "y"

    if word.endswith("s"):
        return word[:-1]

    return word