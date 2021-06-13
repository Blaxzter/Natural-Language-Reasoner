from collections import defaultdict
from logics.logic_functions.Rule import Rule
from logics.senteces.ConnectedExpression import ConnectedExpression


class OrRule(Rule):

    def __init__(self, expression, resulting_expression_1, resulting_expression_2):
        self.name = 'Or Rule'
        self.applicable = 'Or Rule'
        self.description = 'When the sentence connects to expressions with or.'
        self.expression = expression
        self.resulting_expression_1 = resulting_expression_1
        self.resulting_expression_2 = resulting_expression_2

    def get_explanation(self, applied_rule):
        return dict(
            name = self.name,
            description = self.description,
            basic_in_expression = ["Expression 1 OR Expression 2"],
            basic_out_expression = [["Expression 1"], ["Expression 1"]],
            in_expression = [self.expression],
            out_expression = [[self.resulting_expression_1], [self.resulting_expression_2]],
        )

    @staticmethod
    def apply_rule(clause: ConnectedExpression, *args):
        new_clauses = defaultdict(list)

        if type(clause) is not ConnectedExpression:
            return new_clauses, None

        if clause.negated is True or clause.connection_keyword != 'or':
            return new_clauses, None

        left_exp = clause.left_expression.copy()
        right_exp = clause.right_expression.copy()
        new_clauses[0] = [left_exp]
        new_clauses[1] = [right_exp]

        return new_clauses, OrRule(clause, left_exp, right_exp)
