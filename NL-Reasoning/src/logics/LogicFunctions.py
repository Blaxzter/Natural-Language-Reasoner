import copy
from collections import defaultdict
from typing import Any, Dict, Callable

from logics.Expression import Expression
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.senteces.WhenExpression import WhenExpression
from utils.utils import swap_exclamation_marks


# Assume simple structure for now with a and b ... no a and b or c and d
# For that we would need to do a binding check or something and convert
# the Expression into a hierarchical structure and call something like is applicable
# In the case of a and b or c and d it would be like this (a and b) or (c and d) and i
# dont think you can apply the and rule here 


def and_rule(clause: ConnectedExpression) -> defaultdict:
    new_clauses = defaultdict(list)

    if type(clause) is not ConnectedExpression:
        return new_clauses

    if clause.negated or clause.connection_keyword != 'and':
        return new_clauses

    new_clauses[0] += [clause.left_expression.copy()]
    new_clauses[0] += [clause.right_expression.copy()]

    return new_clauses


def or_rule(clause: ConnectedExpression) -> defaultdict:
    new_clauses = defaultdict(list)

    if type(clause) is not ConnectedExpression:
        return new_clauses

    if clause.negated is True or clause.connection_keyword != 'or':
        return new_clauses

    new_clauses[0] = [clause.left_expression.copy()]
    new_clauses[1] = [clause.right_expression.copy()]

    return new_clauses


def when_rule(clause: WhenExpression):
    new_clauses = defaultdict(list)

    if type(clause) is not WhenExpression:
        return new_clauses

    copy_of_when_exp = clause.when_expression.reverse_expression()
    new_clauses[0].append(copy_of_when_exp)

    new_clauses[1].append(clause.not_when_expression)
    return new_clauses


def de_morgan_Law(clause: ConnectedExpression) -> defaultdict:
    new_clauses = defaultdict(list)

    if type(clause) is not ConnectedExpression:
        return new_clauses

    if clause.negated is False:
        return new_clauses

    de_morgen = ConnectedExpression(
        not clause.negated,
        clause.left_expression.reverse_expression(),
        clause.right_expression.reverse_expression(),
        "or" if clause.connection_keyword == "and" else "and"
    )

    if clause.connection_keyword == 'and':
        new_clauses[0].append(de_morgen.left_expression)
        new_clauses[1].append(de_morgen.right_expression)

    if clause.contains('or'):
        new_clauses[0].append(de_morgen.left_expression)
        new_clauses[0].append(de_morgen.right_expression)

    return new_clauses


# Order is important, try to not branch to early
rule_set: Dict[Any, Callable[[Any], Dict[Any, Expression]]] = dict(
    de_Morgan_Law = de_morgan_Law,
    and_rule = and_rule,
    or_rule = or_rule,
    when_rule = when_rule,
)


