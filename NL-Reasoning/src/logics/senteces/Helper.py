from logics.Constants import *
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.senteces.FunctionExpression import FunctionExpression
from logics.senteces.ParseExceptions import ParseException
from logics.senteces.QuantifiedExpression import QuantifiedExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from logics.senteces.WhenExpression import WhenExpression

import re

creating_structures = [
    (QuantifiedExpression, quantified_regex),
    (FunctionExpression, function_regex),
    (SyllogismExpression, syllogism_regex_complete),
    (WhenExpression, when_regex),
    (ConnectedExpression, connected_regex),
    (BaseExpression, None),
]

def create_expression(hypothesis):
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


def create_expression_representation(expression, ret_list = None):
    if ret_list is None:
        ret_list = dict()

    ret_list["list"] = []
    if expression.negated and type(expression) != FunctionExpression:
        ret_list["list"].append(dict(
            type = -1,
            tokens = expression.negated
        ))

    if type(expression) == SyllogismExpression:
        ret_list['type'] = 1
        ret_list['name'] = "Syllogism"
        ret_list['tokens'] = separator.join(expression.tokens)
        return ret_list
    elif type(expression) == ConnectedExpression:
        ret_list['type'] = 2
        ret_list['name'] = "Connected Expression"
        ret_list["list"].append(create_expression_representation(expression.left_expression, dict()))
        ret_list["list"].append(dict(
            type = -2,
            tokens = expression.connection_keyword
        ))
        ret_list["list"].append(create_expression_representation(expression.right_expression, dict()))
        return ret_list
    elif type(expression) == WhenExpression:
        ret_list['type'] = 3
        ret_list['name'] = f"{'Left' if expression.left_match else 'Right'} Conditional Expression"
        if expression.left_match:
            ret_list["list"].append(dict(
                type = -3,
                tokens = expression.key_words[0]
            ))
        ret_list["list"].append(create_expression_representation(expression.when_expression, dict()))
        ret_list["list"].append(dict(
            type = -3,
            tokens = expression.key_words[1 if expression.left_match else 0]
        ))
        ret_list["list"].append(create_expression_representation(expression.not_when_expression, dict()))
        return ret_list

    elif type(expression) == QuantifiedExpression:
        ret_list['type'] = 4
        ret_list['name'] = "For all Expression" if expression.for_all else "It Exists Expression"
        ret_list["list"].append(dict(
            type = -4,
            tokens = expression.quantification_sentence,
        ))
        ret_list["list"].append(dict(
            type = -4,
            name = "Variable",
            tokens = expression.quantified_variable
        ))
        ret_list["list"].append(dict(
            type = -4,
            tokens = expression.quantification_split
        ))
        ret_list["list"].append(create_expression_representation(expression.quantified_expression, dict()))
        return ret_list
    elif type(expression) == BaseExpression:
        ret_list['type'] = 5
        ret_list['name'] = "Basis Information"
        ret_list['tokens'] = separator.join(expression.tokens)
        return ret_list
    elif type(expression) == FunctionExpression:
        ret_list['type'] = 6
        ret_list['name'] = f"{'F' if not expression.multi else 'Multif'}unction Expression{'*' if expression.negated else ''}"
        ret_list["list"].append(dict(
            type = -6,
            name = "Variable",
            tokens = expression.variables[0]
        ))
        ret_list["list"].append(dict(
            type = -6,
            tokens = expression.key_words[0]
        ))
        ret_list["list"].append(dict(
            type = -6,
            name = "Function",
            tokens = expression.quantified_function
        ))
        if expression.multi:
            ret_list["list"].append(dict(
                type = -6,
                tokens = expression.key_words[1]
            ))
            ret_list["list"].append(dict(
                type = -6,
                name = "Variable",
                tokens = expression.variables[1]
            ))
        return ret_list


def check_if_in(keywords, hypothesis):
    for keyword in keywords:
        if keyword in hypothesis:
            return True
    return False
