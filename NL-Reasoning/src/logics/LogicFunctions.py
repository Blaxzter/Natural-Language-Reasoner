import copy
from collections import defaultdict
from typing import Any, Dict, Callable, List

from logics.Expression import Expression
from logics.senteces.SyllogismExpression import SyllogismExpression
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.senteces.WhenExpression import WhenExpression
from utils.utils import swap_exclamation_marks


# Assume simple structure for now with a and b ... no a and b or c and d
# For that we would need to do a binding check or something and convert
# the Expression into a hierarchical structure and call something like is applicable
# In the case of a and b or c and d it would be like this (a and b) or (c and d) and i
# dont think you can apply the and rule here 

def create_new_object(referenced_object, list_of_new_objects):
    for i in range(10000):
        new_object = f'{referenced_object}_{i}'
        if new_object not in list_of_new_objects:
            list_of_new_objects.append(new_object)
            return new_object
    raise Exception("We dont have any new objects left... sorry.")


def and_rule(clause: ConnectedExpression, *args) -> defaultdict:
    new_clauses = defaultdict(list)

    if type(clause) is not ConnectedExpression:
        return new_clauses

    if clause.negated or clause.connection_keyword != 'and':
        return new_clauses

    new_clauses[0] += [clause.left_expression.copy()]
    new_clauses[0] += [clause.right_expression.copy()]

    return new_clauses


def or_rule(clause: ConnectedExpression, *args) -> defaultdict:
    new_clauses = defaultdict(list)

    if type(clause) is not ConnectedExpression:
        return new_clauses

    if clause.negated is True or clause.connection_keyword != 'or':
        return new_clauses

    new_clauses[0] = [clause.left_expression.copy()]
    new_clauses[1] = [clause.right_expression.copy()]

    return new_clauses


def when_rule(clause: WhenExpression, *args):
    new_clauses = defaultdict(list)

    if type(clause) is not WhenExpression:
        return new_clauses

    copy_of_when_exp = clause.when_expression.reverse_expression()
    new_clauses[0].append(copy_of_when_exp)

    new_clauses[1].append(clause.not_when_expression)
    return new_clauses


def de_morgan_Law(clause: ConnectedExpression, *args) -> defaultdict:
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


def syllogism_rule_1(clause: SyllogismExpression, *args) -> defaultdict:
    new_clauses = defaultdict(list)
    if type(clause) is not SyllogismExpression:
        return new_clauses

    if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'all':
        return new_clauses

    # Go over each class and search for a matching syllogism expression
    for comp_clause in args[0]:
        if type(comp_clause) is not SyllogismExpression:
            continue
        if not comp_clause.is_individual:
            continue

        if clause.object != comp_clause.subject:
            continue

        new_clauses[0] = [SyllogismExpression(
            False,
            True,
            comp_clause.individual_keyword,
            comp_clause.object,
            clause.subject,
        )]
        break
    return new_clauses


def syllogism_rule_2(clause: SyllogismExpression, *args) -> defaultdict:
    new_clauses = defaultdict(list)
    if type(clause) is not SyllogismExpression:
        return new_clauses

    if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'some':
        return new_clauses

    first_individual_keyword = ['is', 'a']
    second_individual_keyword = ['is', 'a']
    if 'not' in clause.syllogism_keyword[1]:
        second_individual_keyword.insert(1, 'not')

    new_clauses[0] += [SyllogismExpression(
        False,
        True,
        first_individual_keyword,
        create_new_object(clause.object, args[1]),
        clause.object
    )]
    new_clauses[0] += [SyllogismExpression(
        False,
        True,
        second_individual_keyword,
        create_new_object(clause.subject, args[1]),
        clause.subject
    )]
    return new_clauses


def syllogism_rule_3(clause: SyllogismExpression, *args) -> defaultdict:
    new_clauses = defaultdict(list)
    if type(clause) is not SyllogismExpression:
        return new_clauses

    if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'no':
        return new_clauses

    # Go over each class and search for a matching syllogism expression
    for comp_clause in args[0]:
        if type(comp_clause) is not SyllogismExpression:
            continue
        if not comp_clause.is_individual:
            continue

        if clause.object != comp_clause.subject:
            continue

        individual_keyword = comp_clause.individual_keyword
        individual_keyword.insert(1, 'not')
        new_clauses[0] = [SyllogismExpression(
            False,
            True,
            individual_keyword,
            comp_clause.subject,
            clause.subject,
        )]
        break
    return new_clauses


def syllogism_reverse_rule(clause: SyllogismExpression, *args):
    new_clauses = defaultdict(list)
    if type(clause) is not SyllogismExpression:
        return new_clauses

    if not clause.negated:
        return new_clauses

    if clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'all':
        new_clauses[0] += [SyllogismExpression(
            False,
            False,
            ("some", ['are', 'not']),
            clause.object,
            clause.subject,
        )]
    elif clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'some':
        new_clauses[0] += [SyllogismExpression(
            False,
            False,
            ("no", ['is']),
            clause.object,
            clause.subject,
        )]
    elif clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'no':
        new_clauses[0] += [SyllogismExpression(
            False,
            False,
            ("some", ['are']),
            clause.object,
            clause.subject,
        )]
    elif clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'no':
        new_clauses[0] += [SyllogismExpression(
            False,
            False,
            ("all", ['are']),
            clause.object,
            clause.subject,
        )]
    return new_clauses


# Order is important, try to not branch to early
rule_set: Dict[Any, Callable[[Any, List, List], Dict[Any, Expression]]] = dict(
    and_rule = and_rule,
    de_Morgan_Law = de_morgan_Law,
    or_rule = or_rule,
    when_rule = when_rule,

    syllogism_reverse_rule = syllogism_reverse_rule,
    syllogism_rule_1 = syllogism_rule_1,
    syllogism_rule_2 = syllogism_rule_2,
    syllogism_rule_3 = syllogism_rule_3,
)


