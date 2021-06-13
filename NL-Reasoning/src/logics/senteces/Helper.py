from logics.Constants import *
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.senteces.QuantifiedExpression import QuantifiedExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from logics.senteces.WhenExpression import WhenExpression

import re

def create_expression(hypothesis):
    lower = hypothesis.lower()

    creating_structures = [
        (quantified_keywords, QuantifiedExpression, None),
        (syllogism_keywords, SyllogismExpression, syllogism_regex),
        (when_keywords, WhenExpression, None),
        (connection_keywords, ConnectedExpression, None),
    ]

    error_list = []

    for creating_structure in creating_structures:
        if check_if_in(creating_structure[0], lower):
            if creating_structure[2] is not None:
                if re.match(creating_structure[2], lower, re.IGNORECASE):
                    try:
                        expression = creating_structure[1](lower)
                        return expression
                    except Exception as err:
                        error_list.append(err)
            else:
                try:
                    expression = creating_structure[1](lower)
                    return expression
                except Exception as err:
                    error_list.append(err)
    try:
        expression = BaseExpression(lower)
        return expression
    except Exception as err:
        error_list.append(err)
        return error_list


def create_expression_representation(expression, ret_list = None):
    if ret_list is None:
        ret_list = dict()

    ret_list["list"] = []
    if expression.negated:
        ret_list["list"].append(dict(
            type = -1,
            name = expression.negated
        ))

    if type(expression) == SyllogismExpression:
        ret_list['type'] = 0
        ret_list['name'] = "Syllogism"
        ret_list['tokens'] = separator.join(expression.tokens)
        return ret_list
    elif type(expression) == ConnectedExpression:
        ret_list['type'] = 1
        ret_list['name'] = "Connected Expression"
        ret_list["list"].append(create_expression_representation(expression.left_expression, dict()))
        ret_list["list"].append(dict(
            type = 5,
            name = expression.connection_keyword
        ))
        ret_list["list"].append(create_expression_representation(expression.right_expression, dict()))
        return ret_list
    elif type(expression) == WhenExpression:
        ret_list['type'] = 2
        ret_list['name'] = "Conditional Expression"
        ret_list["list"].append(dict(
            type = 6,
            name = expression.when_keyword
        ))
        ret_list["list"].append(create_expression_representation(expression.when_expression, dict()))
        ret_list["list"].append(dict(
            type = 6,
            name = expression.when_split_token
        ))
        ret_list["list"].append(create_expression_representation(expression.not_when_expression, dict()))
        return ret_list
    elif type(expression) == QuantifiedExpression:
        ret_list['type'] = 3
        ret_list['name'] = "For all Expression" if expression.for_all else "It Exists Expression"
        ret_list["list"].append(dict(
            type = 7,
            name = separator.join(expression.quantified_sentence),
        ))
        ret_list["list"].append(dict(
            type = 7,
            name = "Variable",
            tokens = expression.quantified_variable
        ))
        ret_list["list"].append(create_expression_representation(expression.quantified_expression, dict()))
        return ret_list
    elif type(expression) == BaseExpression:
        ret_list['type'] = 4
        ret_list['name'] = "Basis Information"
        ret_list['tokens'] = separator.join(expression.tokens)
        return ret_list


def check_if_in(keywords, hypothesis):
    for keyword in keywords:
        if keyword in hypothesis:
            return True
    return False
