from collections import defaultdict
from logics.senteces.WhenExpression import WhenExpression
from logics.senteces.ConnectedExpression import ConnectedExpression


class WhenRule:

    def __init__(self):
        self.name = 'When Rule'
        self.applicable = 'When Rule'

    def get_explanation(self, applied_rule):
        return f'html rule'

    def apply_rule(self, clause: WhenExpression, *args):
        new_clauses = defaultdict(list)

        if type(clause) is not WhenExpression:
            return new_clauses

        copy_of_when_exp = clause.when_expression.reverse_expression()
        new_clauses[0].append(copy_of_when_exp)

        new_clauses[1].append(clause.not_when_expression)
        return new_clauses