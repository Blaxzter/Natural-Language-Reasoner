from logics.Constants import *
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from logics.senteces.WhenExpression import WhenExpression
from utils.utils import tokenize


def create_expression(hypothesis):
    tokenized = tokenize(hypothesis.lower())

    if check_if_in(syllogism_keywords, tokenized):
        return SyllogismExpression(tokenized)
    if check_if_in(when_keywords, tokenized):
        return WhenExpression(tokenized)
    if check_if_in(connection_keywords, tokenized):
        return ConnectedExpression(tokenized)

    return BaseExpression(tokenized)


def create_expression_representation(expression, ret_list = None):
    if ret_list is None:
        ret_list = list()

    if expression.negated:
        ret_list.append(dict(
            type = -1,
            name = expression.negated
        ))

    if type(expression) == SyllogismExpression:
        ret_list.append(dict(
            type = -1,
            name = expression.negated
        ))
        ret_list.append(dict(
            type = 0,
            name = "Syllogism"
        ))
        return ret_list
    elif type(expression) == ConnectedExpression:
        ret_list.append(dict(
            type = -1,
            name = expression.negated
        ))
        create_expression_representation(expression.left_expression, ret_list)
        ret_list.append(dict(
            type = 6,
            name = expression.connection_keyword
        ))
        create_expression_representation(expression.left_expression, ret_list)
        return ret_list
    elif type(expression) == WhenExpression:
        ret_list.append(dict(
            type = -1,
            name = expression.negated
        ))
        ret_list.append(dict(
            type = 6,
            name = expression.when_keyword
        ))
        create_expression_representation(expression.when_expression, ret_list)
        ret_list.append(dict(
            type = 6,
            name = expression.when_split_token
        ))
        create_expression_representation(expression.not_when_expression, ret_list)
        return ret_list

    elif type(expression) == BaseExpression:
        ret_list.append(dict(
            type = -1,
            name = expression.negated
        ))
        ret_list.append(dict(
            type = 6,
            name = "Base Expression"
        ))
        return ret_list


def check_if_in(keywords, hypothesis):
    for keyword in keywords:
        if keyword in hypothesis:
            return True
    return False
