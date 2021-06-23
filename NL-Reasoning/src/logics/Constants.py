"""
This file is where the magic happens
All the constants and regex expressions are defined

I explain every line as every variable is quite self explanatory
"""

match_types = ["optional", "once", "at_least_once"]

def or_reg(keyword_list, match_type = "once"):
    """
    Function that given a keyword list creates the regex or operator
    :param keyword_list: The keyword list
    :param match_type: If the operator is required or optional
    :return: (keyword_1|keyword_2)match_type
    """

    sorted_by_length = sorted(keyword_list, key = len, reverse = True)

    ret_regex = "("
    for i, key_word in enumerate(sorted_by_length):
        ret_regex += key_word
        if i != len(sorted_by_length) - 1:
            ret_regex += "|"

    ret_regex += ")"
    if match_type == match_types[0]:
        ret_regex += "?"
    elif match_type == match_types[1]:
        ret_regex += ""
    else:
        ret_regex += "+"
    return ret_regex


complete_negation = 'it is not the case that'
complete_negation_tokens = ['it', 'is', 'not', 'the', 'case', 'that']
base_regex = f"({complete_negation} )?"

separator = ' '

negation_keywords = [['do', 'not'], ['does', 'not'], 'not', 'never', 'dont', 'don\'t', 'doesnt', 'doesn\'t']
base_filler_words = ['the', 'must', 'a']

connection_keywords = ['or', 'and', ';', 'nor']
and_connection_keywords = ['and', ';']
or_connection_keywords = ['or', 'nor']

demoregen_regex = "Neither [a-zA-Z0-9 -]+ (nor|and|or) [a-zA-Z0-9 -]+"
true_connected_regex = "[a-zA-Z0-9 -]+ (or|and|;) [a-zA-Z0-9 -]+"
connected_regex = f"{base_regex}({demoregen_regex}|{true_connected_regex})"

# When keywords and regex
when_keywords = ['when', 'if']
when_split_tokens = [',', 'then', ', then']
when_split_right = ['because', ', because', 'if', ', if', ', because of']
when_left_regex = f"{or_reg(when_keywords)} [a-zA-Z0-9 -]+{or_reg(when_split_tokens)} [a-zA-Z0-9, -]+"
when_right_regex = f"[a-zA-Z0-9 -]+{or_reg(when_split_right)} [a-zA-Z0-9 -]+"
when_regex = f"{base_regex}({when_left_regex}|{when_right_regex})"

de_morgen_expression = 'neither'

pluralism_keywords = ['all', 'some', 'no']
pos_middle_keywords = ["have", "are", "is an", "is a", "is", "has"]
neg_middle_keywords = ["have not",  "are not", "is not an", "is not a", "is not", "has not"]


def get_opposite_of(middle_keyword):
    if middle_keyword in pos_middle_keywords:
        position = pos_middle_keywords.index(middle_keyword)
        return neg_middle_keywords[position]

    if middle_keyword in neg_middle_keywords:
        position = neg_middle_keywords.index(middle_keyword)
        return pos_middle_keywords[position]


middle_keywords = pos_middle_keywords + neg_middle_keywords
syllogism_regex = f"{or_reg(pluralism_keywords)} [a-zA-Z0-9 -]+ {or_reg(middle_keywords)} .+"
conclusion_regex = "(Therefore, )?"
syllogism_regex_complete = f"{conclusion_regex}{base_regex}{syllogism_regex}"


pos_function_keywords = ["is the", "is an", "is a", "is", "are"]
neg_function_keywords = ["is not the", "is not an", "is not a", "is not", "are not"]

def get_opposite_of_function(middle_keyword):
    if middle_keyword in pos_function_keywords:
        position = pos_function_keywords.index(middle_keyword)
        return neg_function_keywords[position]

    if middle_keyword in neg_function_keywords:
        position = neg_function_keywords.index(middle_keyword)
        return pos_function_keywords[position]

function_keywords = pos_function_keywords + neg_function_keywords
function_split_keywords = ["than", "of"]
single_function_regex = f"[a-zA-Z0-9-]+ {or_reg(function_keywords)} [a-zA-Z0-9-]+"
multi_function_regex = f"[a-zA-Z0-9-]+ {or_reg(function_keywords)} [a-zA-Z0-9-]+ {or_reg(function_split_keywords)} [a-zA-Z0-9-]+"
function_regex = f"{base_regex}({multi_function_regex}|{single_function_regex})"

quantified_keywords_plural = ['For each', 'For all']
quantified_keywords_singular = ['There is a', 'It exists a']
quantified_keywords_split = [',', ' ,', ' it is the case that', '\s']
quantified_keywords = quantified_keywords_plural + quantified_keywords_singular
quantified_regex_plural = f"{or_reg(quantified_keywords_plural)} [a-zA-Z0-9-]+{or_reg(quantified_keywords_split, match_types[0])}.+"
quantified_regex_singular = f"{or_reg(quantified_keywords_singular)} [a-zA-Z0-9-]+{or_reg(quantified_keywords_split, match_types[0])}.+"
quantified_regex = f"{base_regex}({quantified_regex_plural}|{quantified_regex_singular})"
