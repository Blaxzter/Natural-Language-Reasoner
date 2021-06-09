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


def check_if_in(keywords, hypothesis):
    for keyword in keywords:
        if keyword in hypothesis:
            return True
    return False
