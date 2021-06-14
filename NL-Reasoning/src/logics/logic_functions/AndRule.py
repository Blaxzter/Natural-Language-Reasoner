from collections import defaultdict

from logics.logic_functions.Rule import Rule
from logics.senteces.ConnectedExpression import ConnectedExpression


class AndRule(Rule):

    def __init__(self, expression, resulting_expression_1, resulting_expression_2):
        self.name = 'And Rule'
        self.applicable = 'And Rule'
        self.description = '(A AND B) => add to its leaf the chain of two nodes containing both arguments A, B'
        self.expression = expression
        self.resulting_expression_1 = resulting_expression_1
        self.resulting_expression_2 = resulting_expression_2

    def get_explanation(self, applied_rule):
        return dict(
            name = self.name,
            description = self.description,
            in_expression = [self.expression.get_string_rep()],
            out_expression = [[self.resulting_expression_1.get_string_rep(), self.resulting_expression_2.get_string_rep()]],
        )

    @staticmethod
    def apply_rule(clause: ConnectedExpression, *args):
        new_clauses = defaultdict(list)

        if type(clause) is not ConnectedExpression:
            return new_clauses, None

        if clause.negated or clause.connection_keyword != 'and':
            return new_clauses, None

        left_exp = clause.left_expression.copy()
        right_exp = clause.right_expression.copy()
        new_clauses[0] += [left_exp]
        new_clauses[0] += [right_exp]

        return new_clauses, AndRule(clause, left_exp, right_exp)