
from collections import defaultdict
from typing import Any, Dict, Callable

from logics.Expression import Expression


# Assume simple structure for now with a and b ... no a and b or c and d
# For that we would need to do a binding check or something and convert
# the Expression into a hierarchical structure and call something like is applicable
# In the case of a and b or c and d it would be like this (a and b) or (c and d) and i
# dont think you can apply the and rule here


def simple_split_rule(clause: Expression, split_token: str):
    # if the rule is not applicable then return empty list
    if not clause.is_applicable(split_token):
        return []

    index_of_rule = clause.get_applicable_token(split_token)
    return [Expression(clause.tokens[:index_of_rule]), Expression(clause.tokens[index_of_rule + 1:])]


def and_rule(clause: Expression) -> defaultdict:
    new_clauses = defaultdict(list)

    split_token = 'and'
    split_expressions = simple_split_rule(clause, split_token)
    if len(split_expressions) != 0:
        new_clauses[0] += split_expressions
    return new_clauses


def or_rule(clause: Expression) -> defaultdict:
    new_clauses = defaultdict(list)

    split_token = 'or'
    split_expressions = simple_split_rule(clause, split_token)
    for i, split_expression in enumerate(split_expressions):
        new_clauses[i].append(split_expression)
    return new_clauses


def when_rule(clause: Expression):
    new_clauses = defaultdict(list)

    if not clause.is_applicable('when'):
        return new_clauses

    split_index = clause.get_applicable_token('when')
    left_tokens = list(clause.tokens[:split_index])
    right_tokens = list(clause.tokens[split_index + 1:])

    if 'when' in left_tokens:
        when_token = left_tokens
        not_when_token = right_tokens
    else:
        not_when_token = left_tokens
        when_token = right_tokens

    when_token.remove('when')
    when_expression = Expression(when_token)
    when_expression.reverse_expression()
    new_clauses[0].append(when_expression)
    new_clauses[1].append(Expression(not_when_token))
    return new_clauses


# Order is important, try to not branch to early
rule_set: Dict[Any, Callable[[Expression], Dict[Any, Expression]]] = dict(
    and_rule = and_rule,
    or_rule = or_rule,
    when_rule = when_rule,
)
