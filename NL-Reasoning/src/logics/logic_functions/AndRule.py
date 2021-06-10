from collections import defaultdict

from logics.senteces.ConnectedExpression import ConnectedExpression


class AndRule:

    def __init__(self):
        self.name = 'And Rule'
        self.applicable = 'And Rule'

    def get_explanation(self, applied_rule):
        return f'html rule'

    def apply_rule(self, clause: ConnectedExpression, *args):
        new_clauses = defaultdict(list)

        if type(clause) is not ConnectedExpression:
            return new_clauses

        if clause.negated or clause.connection_keyword != 'and':
            return new_clauses

        new_clauses[0] += [clause.left_expression.copy()]
        new_clauses[0] += [clause.right_expression.copy()]

        return new_clauses