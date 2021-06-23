import inflect


def create_new_object(list_of_new_objects, ref_object = None):
    """
    Function that creates the new object based on the new object list
    :param list_of_new_objects: The previously created new objects
    :param ref_object:          If a reference object is used take that as a name origin
    :return: The new object
    """

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
    """
    Function that goes over the matches of a regex and gets the found keywords and sentences in between
    :param reg_match: The regex match
    :param sentence:  The sentence
    :return: sentences, keywords
    """
    # Filter unnecessary group matches
    reg_groups = list(filter(
        lambda x: not ((x[0] == 0 and x[1] == len(sentence)) or (x[0] == -1 and x[1] == -1)),
        reg_match.regs
    ))

    sentences = []
    key_words = []
    c_index = 0
    # Go over each match
    for group_match in reg_groups:
        l_idx, r_idx = group_match
        curr_sentence = sentence[l_idx:r_idx].strip()
        key_words.append(curr_sentence)
        if l_idx - c_index > 0:
            sentences.append(sentence[c_index:l_idx].strip())
        c_index = r_idx + (1 if len(curr_sentence) != 0 else 0)
    sentences.append(sentence[c_index:])
    return sentences, key_words

exception_tokens = ['is', 'chess', 'poisonous', 'does', 'has']

def single_tokens(sentence_tokens):
    """
    Transforms words in the token list into thier homonogenes self
    :param sentence_tokens:
    :return:
    """
    # Get the inflect engine
    single = inflect.engine()
    single_tokens = []
    for i, token in enumerate(sentence_tokens):
        token_single = single.singular_noun(token)
        if token_single == 'mouses' or token_single == 'mou':
            token_single = 'mouse'
        if token_single != False and token not in exception_tokens:
            single_tokens.append(token_single)
        else:
            single_tokens.append(token)
    return single_tokens


def list_eq_check(element_list, comp_str):
    """
    Check whether a str is in the element list
    :param element_list: The list that is checked
    :param comp_str:     The str to be searched for
    :return: The element if found otherwise None
    """
    for element in element_list:
        if element == comp_str:
            return element
    return None


def list_in_check(element_list, comp_list):
    """
    Check whether a element is in the comp list
    :param element_list: The list that is checked
    :param comp_str:     The comp_list to be searched for
    :return: The element if found otherwise None
    """
    for element in element_list:
        if element in comp_list:
            return element
    return None


def check_if_list_in_list(check_list, reference_list):
    """
    We search whether the check list occures in the reference list
    :param check_list:      The list to be searched for in the reference list
    :param reference_list:  The reference list
    :return: True when the list is in the list otherwise false.
    """
    search_index = 0
    while True:
        if check_list[0] in reference_list[search_index:]:
            first_index = reference_list[search_index:].index(check_list[0])
            found = True
            for i, tokens in enumerate(check_list[1:]):
                if reference_list[search_index:][first_index + (i + 1)] != tokens:
                    found = False
                    break
            if found:
                return search_index + first_index
            else:
                search_index = first_index + 1
        else:
            return None

def tokenize(sentence: str):
    """
    Tokenizer of the sentence
    :param sentence: The input sentence
    :return: The tokenized sentence
    """
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

