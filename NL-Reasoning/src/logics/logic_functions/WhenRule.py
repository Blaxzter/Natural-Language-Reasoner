from collections import defaultdict
from logics.senteces.WhenExpression import WhenExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.logic_functions.Rule import Rule

class WhenRule(Rule):

    def __init__(self, expression, resulting_expression_1, resulting_expression_2):
        self.name = 'When Rule'
        self.applicable = 'When Rule'
        self.description = '(When A then B) = (If A then B) = (Not A OR B) => Create two sibling leaf to the branch containing Not A, B, respectively'
        self.expression = expression
        self.resulting_expression_1 = resulting_expression_1
        self.resulting_expression_2 = resulting_expression_2


    def get_explanation(self, applied_rule):
        return dict(
            name=self.name,
            description=self.description,
            in_expression=[self.expression.get_string_rep()],
            out_expression=[
                [self.resulting_expression_1.get_string_rep(), self.resulting_expression_2.get_string_rep()]],
        )

    @staticmethod
    def apply_rule(clause: WhenExpression, *args):
        new_clauses = defaultdict(list)

        if type(clause) is not WhenExpression:
            return new_clauses, None

        copy_of_when_exp = clause.when_expression.reverse_expression()
        new_clauses[0].append(copy_of_when_exp)

        new_clauses[1].append(clause.not_when_expression)
        return new_clauses, WhenRule(clause, copy_of_when_exp, clause.not_when_expression)