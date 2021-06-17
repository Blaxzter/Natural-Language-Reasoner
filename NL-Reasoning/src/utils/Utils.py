import inflect


def create_new_object(list_of_new_objects, ref_object = None):

    if len(list_of_new_objects) == 0 and ref_object is None:
        list_of_new_objects.append("There")
        return "There"

    for i in range(1, 10000):
        new_object = f'{ref_object if ref_object is not None else "Object"}_{i}'
        if new_object not in list_of_new_objects:
            list_of_new_objects.append(new_object)
            return new_object
    raise Exception("We dont have any new objects left... sorry.")


def get_sentences_key_words(reg_match, sentence):
    # Filter unnecessary group matches
    reg_groups = list(filter(
        lambda x: not ((x[0] == 0 and x[1] == len(sentence)) or (x[0] == -1 and x[1] == -1)),
        reg_match.regs
    ))

    sentences = []
    key_words = []
    c_index = 0
    for group_match in reg_groups:
        l_idx, r_idx = group_match
        curr_sentence = sentence[l_idx:r_idx].strip()
        key_words.append(curr_sentence)
        if l_idx - c_index > 0:
            sentences.append(sentence[c_index:l_idx].strip())
        c_index = r_idx + (1 if len(curr_sentence) != 0 else 0)
    sentences.append(sentence[c_index:])
    return sentences, key_words


def single_tokens(sentence_tokens):
    single = inflect.engine()
    single_tokens = []
    for i, token in enumerate(sentence_tokens):
        token_single = single.singular_noun(token)
        if token_single != False and token != 'is' and token != 'chess' and token != 'poisonous':
            single_tokens.append(token_single)
        else:
            single_tokens.append(token)
    return single_tokens


def list_eq_check(element_list, comp_str):
    for element in element_list:
        if element == comp_str:
            return element
    return None


def list_in_check(element_list, comp_list):
    for element in element_list:
        if element in comp_list:
            return element
    return None


def tokenize(sentence: str):
    tokens = sentence.split(" ")
    ret_tokens = []
    for i, token in enumerate(tokens):
        if ',' in token or '!' in token or ')' in token or '(' in token:
            if ',' in token:
                c_token = token.split(',')
                if len(c_token[0]) != 0:
                    ret_tokens.append(c_token[0])
                ret_tokens.append(',')
            if '!(' in token:
                c_token = token.split('!(')
                ret_tokens.append('!')
                ret_tokens.append('(')
                ret_tokens.append(c_token[1])
            elif '!' in token:
                c_token = token.split('!')
                ret_tokens.append('!')
                ret_tokens.append(c_token[1])
            if ')' in token:
                c_token = token.split(')')
                ret_tokens.append(c_token[0])
                ret_tokens.append(')')
        else:
            ret_tokens.append(token)
    ret_tokens = single_tokens(ret_tokens)
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

def swap_exclamation_marks(sentence_tokens):
    if '(' in sentence_tokens:
        sentence_tokens.remove('(')
    if ')' in sentence_tokens:
        sentence_tokens.remove(')')
    if '!' in sentence_tokens:
        sentence_tokens.remove('!')

    sentence_type = detect_sentence_structure(sentence_tokens)

    if sentence_type == 1 or 2:
        sentence_tokens.insert(2, "not")
    elif sentence_type == 2 or 4:
        sentence_tokens.remove("not")

    return sentence_tokens


