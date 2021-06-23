from logics.Constants import *
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.senteces.FunctionExpression import FunctionExpression
from logics.senteces.ParseExceptions import ParseException
from logics.senteces.QuantifiedExpression import QuantifiedExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from logics.senteces.WhenExpression import WhenExpression

import re

# List of expressions and their matched regex that we support
creating_structures = [
    (QuantifiedExpression, quantified_regex),
    (FunctionExpression, function_regex),
    (SyllogismExpression, syllogism_regex_complete),
    (WhenExpression, when_regex),
    (ConnectedExpression, connected_regex),
    (BaseExpression, None),
]


def create_expression(hypothesis):
    """
    Function that creates the expressions given a sentence
    If no match is found return a parse expression
    :param hypothesis: The sentence
    :return: The create expression
    """
    lower = hypothesis.strip().lower()

    error_list = []

    # We go over each element in the creating structure and check for the regular expression
    # We only want full matches
    for constructor, expression_regex in creating_structures:
        regex_match = None
        if expression_regex is not None:
            regex_match = re.match(expression_regex, lower, re.IGNORECASE)
        if expression_regex is None or (regex_match and regex_match.end() == len(lower)):
            try:
                expression = constructor(lower)
                return expression
            except Exception as err:
                if type(err) is ParseException:
                    error_list += err.exception_list
                else:
                    error_list.append(str(err))

    if len(error_list) != 0:
        raise ParseException(error_list)


def create_expression_representation(expression, ret_dict = None):
    """
    Recursive function that creates the data structure for the language checker
    :param expression: The expression to be parsed
    :param ret_dict: The dictionary as the data structure
    :return: The created data structure
    """
    if ret_dict is None:
        ret_dict = dict()

    ret_dict["list"] = []
    if expression.negated and type(expression) != FunctionExpression:
        ret_dict["list"].append(dict(
            type = 0,
            tokens = expression.negated
        ))

    if type(expression) == SyllogismExpression:
        ret_dict['type'] = 1
        ret_dict['name'] = "Syllogism"
        ret_dict["list"].append(dict(
            type = -1,
            name = "1. Keyword",
            tokens = expression.syllogism_keywords[0],
        ))
        ret_dict["list"].append(dict(
            type = -1,
            name = "Object",
            tokens = expression.object
        ))
        ret_dict["list"].append(dict(
            type = -1,
            name = "2. Keyword",
            tokens = expression.syllogism_keywords[1]
        ))
        ret_dict["list"].append(dict(
            type = -1,
            name = "Subject",
            tokens = expression.subject
        ))
        return ret_dict
    elif type(expression) == ConnectedExpression:
        ret_dict['type'] = 2
        ret_dict['name'] = "Connected Expression"
        ret_dict["list"].append(create_expression_representation(expression.left_expression, dict()))
        ret_dict["list"].append(dict(
            type = -2,
            tokens = expression.connection_keyword
        ))
        ret_dict["list"].append(create_expression_representation(expression.right_expression, dict()))
        return ret_dict
    elif type(expression) == WhenExpression:
        ret_dict['type'] = 3
        ret_dict['name'] = f"{'Left' if expression.left_match else 'Right'} Conditional Expression"
        if expression.left_match:
            ret_dict["list"].append(dict(
                type = -3,
                tokens = expression.key_words[0]
            ))
        ret_dict["list"].append(create_expression_representation(expression.when_expression, dict()))
        ret_dict["list"].append(dict(
            type = -3,
            tokens = expression.key_words[1 if expression.left_match else 0]
        ))
        ret_dict["list"].append(create_expression_representation(expression.not_when_expression, dict()))
        return ret_dict

    elif type(expression) == QuantifiedExpression:
        ret_dict['type'] = 4
        ret_dict['name'] = "For all Expression" if expression.for_all else "It Exists Expression"
        ret_dict["list"].append(dict(
            type = -4,
            tokens = expression.quantification_sentence,
        ))
        ret_dict["list"].append(dict(
            type = -4,
            name = "Variable",
            tokens = expression.quantified_variable
        ))
        ret_dict["list"].append(dict(
            type = -4,
            tokens = expression.quantification_split
        ))
        ret_dict["list"].append(create_expression_representation(expression.quantified_expression, dict()))
        return ret_dict
    elif type(expression) == BaseExpression:
        ret_dict['type'] = 5
        ret_dict['name'] = "Basis Information"
        ret_dict["list"].append(dict(
            type = -5,
            name = "Subject",
            tokens = expression.subject,
        ))
        ret_dict["list"].append(dict(
            type = -5,
            name = "Verb",
            tokens = expression.verb
        ))
        ret_dict["list"].append(dict(
            type = -5,
            name = "Object",
            tokens = expression.object
        ))
        return ret_dict
    elif type(expression) == FunctionExpression:
        ret_dict['type'] = 6
        ret_dict['name'] = f"{'F' if not expression.multi else 'Multif'}unction Expression{'*' if expression.negated else ''}"
        ret_dict["list"].append(dict(
            type = -6,
            name = "Variable",
            tokens = expression.variables[0]
        ))
        ret_dict["list"].append(dict(
            type = -6,
            tokens = expression.key_words[0]
        ))
        ret_dict["list"].append(dict(
            type = -6,
            name = "Function",
            tokens = expression.quantified_function
        ))
        if expression.multi:
            ret_dict["list"].append(dict(
                type = -6,
                tokens = expression.key_words[1]
            ))
            ret_dict["list"].append(dict(
                type = -6,
                name = "Variable",
                tokens = expression.variables[1]
            ))
        return ret_dict


def check_if_in(keywords, hypothesis):
    """
    Simple function that checks whether a keyword is in the hypothesis
    :param keywords:    The keywords
    :param hypothesis:  The sentence
    :return: True if a keyword is in the sentence
    """
    for keyword in keywords:
        if keyword in hypothesis:
            return True
    return False
