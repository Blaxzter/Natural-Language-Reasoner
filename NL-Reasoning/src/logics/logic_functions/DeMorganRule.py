from collections import defaultdict
from logics.logic_functions.Rule import Rule
from logics.senteces.ConnectedExpression import ConnectedExpression


class DeMorganRule(Rule):

    def __init__(self):
        self.name = 'De Morgan Law Rule'
        self.applicable = 'De Morgan Law Rule'

    def get_explanation(self, applied_rule):
        return f'html rule'

    def apply_rule(self, clause: ConnectedExpression, *args):
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
