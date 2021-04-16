def tokenize(sentence: str):
    tokens = sentence.split(" ")
    ret_tokens = []
    for i, token in enumerate(tokens):
        if ',' in token:
            c_token = token.split(',')
            ret_tokens.append(c_token[0])
            ret_tokens.append(',')
        else:
            ret_tokens.append(token)

    return ret_tokens


def detect_sentence_structure(sentence_tokens):
    if sentence_tokens is None or type(sentence_tokens) is not list or len(sentence_tokens) == 0:
        raise ValueError("Sentence structure detection only works for token lists. "
                         "And the token list is not empty")

    # TODO support multiple sentence base structures
    # does not play vs plays not ...
    # TODO maybe we need to do a bit more elaborate approach besides the length

    # Basic structure: A is B
    if len(sentence_tokens) == 3 and sentence_tokens[1] == "is":
        return 1

    # Basic structure: A does B
    if len(sentence_tokens) == 3:
        return 2

    # Inverted basic structure: A is not B
    if len(sentence_tokens) == 4 and sentence_tokens[1] == "is":
        return 3

    # Inverted basic structure: A does not B
    # Split because maybe we want to check: A does not do B or doesn't
    if len(sentence_tokens) == 4:
        return 4

    raise ValueError(f'Sentence structure is not detected: {str(sentence_tokens)}')
