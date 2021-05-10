
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

    if not (clause.is_applicable('when') or clause.is_applicable('if')):
        return new_clauses
    elif clause.is_applicable('when'):
        split_index = clause.get_applicable_token('when')
    elif clause.is_applicable('if'):
        split_index = clause.get_applicable_token('if')

    left_tokens = list(clause.tokens[:split_index])
    right_tokens = list(clause.tokens[split_index + 1:])

    if 'when' in left_tokens:
        when_token = left_tokens
        not_when_token = right_tokens
    elif 'if' in left_tokens:
        when_token = left_tokens
        not_when_token = right_tokens
    else:
        not_when_token = left_tokens
        when_token = right_tokens

    if 'when' in when_token:
        when_token.remove('when')
    else:
        when_token.remove('if')

    when_expression = Expression(when_token)
    when_expression.reverse_expression()
    new_clauses[0].append(when_expression)
    new_clauses[1].append(Expression(not_when_token))
    return new_clauses


def de_Morgan_Law(clause: Expression) -> defaultdict:
    new_clauses = defaultdict(list)

    if not clause.is_applicable('deMorgan'):
        return new_clauses

    if clause.contains('and'):
        split_index = clause.get_applicable_token('and')
        left_tokens = list(clause.tokens[:split_index])
        right_tokens = list(clause.tokens[split_index+1:])

        new_right_tokens = list(left_tokens[:-1])
        new_right_tokens.extend(right_tokens)
        left_tokens.extend([')', 'or'])
        complete_sentence = list(left_tokens)
        complete_sentence.extend(new_right_tokens)

        new_clauses[0].append(left_tokens)
        new_clauses[1].append(new_right_tokens)
        return new_clauses

    if clause.contains('or'):
        split_index = clause.get_applicable_token('or')
        left_tokens = list(clause.tokens[:split_index])
        right_tokens = list(clause.tokens[split_index + 1:])

        new_right_tokens = list(left_tokens[:-1])
        new_right_tokens.extend(right_tokens)
        left_tokens.extend([')', 'and'])
        complete_sentence = list(left_tokens)
        complete_sentence.extend(new_right_tokens)
        new_clauses[0].append(left_tokens)
        new_clauses[1].append(new_right_tokens)
        for tokens in [left_tokens, new_right_tokens]:
            if len(left_tokens) != 0 and len(new_right_tokens) != 0:
                new_clauses[0] += tokens
        return new_clauses



# Order is important, try to not branch to early
rule_set: Dict[Any, Callable[[Expression], Dict[Any, Expression]]] = dict(
    de_Morgan_Law = de_Morgan_Law,
    and_rule = and_rule,
    or_rule = or_rule,
    when_rule = when_rule,
)


