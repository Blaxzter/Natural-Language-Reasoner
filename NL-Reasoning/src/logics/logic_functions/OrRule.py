from collections import defaultdict
from logics.logic_functions.Rule import Rule
from logics.senteces.ConnectedExpression import ConnectedExpression


class OrRule(Rule):

    def __init__(self):
        self.name = 'Or Rule'
        self.applicable = 'Or Rule'

    def get_explanation(self, applied_rule):
        return f'html rule'

    def apply_rule(self, clause: ConnectedExpression, *args):
        new_clauses = defaultdict(list)

        if type(clause) is not ConnectedExpression:
            return new_clauses

        if clause.negated is True or clause.connection_keyword != 'or':
            return new_clauses

        new_clauses[0] = [clause.left_expression.copy()]
        new_clauses[1] = [clause.right_expression.copy()]

        return new_clauses