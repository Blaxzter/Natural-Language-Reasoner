from collections import defaultdict

from logics.Constants import and_connection_keywords
from logics.logic_functions.Rule import Rule
from logics.senteces.ConnectedExpression import ConnectedExpression


class AndRule(Rule):
    """
    Class representing the application of the and rule.
    It is required for the tool tip
    """

    def __init__(self, expression, resulting_expression_1, resulting_expression_2):
        self.name = 'And Rule'
        self.applicable = 'And Rule'
        self.description = '(A AND B) => add to its leaf the chain of two nodes containing both arguments A, B'
        self.expression = expression
        self.resulting_expression_1 = resulting_expression_1
        self.resulting_expression_2 = resulting_expression_2

    def get_explanation(self):
        """
        :return: Create the explanation based on the provided data in the object.
        """
        return dict(
            name = self.name,
            description = self.description,
            basic_in_expression = ["Expression 1 AND Expression 2"],
            basic_out_expression = [["Expression 1", "Expression 2"]],
            in_expression = [self.expression.get_string_rep()],
            out_expression = [[self.resulting_expression_1.get_string_rep(), self.resulting_expression_2.get_string_rep()]],
        )

    @staticmethod
    def apply_rule(clause: ConnectedExpression, *args):
        """
        Apply the and rule which when applicable splits the b
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """
        new_clauses = defaultdict(list)

        # Do application tests
        if type(clause) is not ConnectedExpression:
            return new_clauses, None

        if clause.negated or clause.connection_keyword not in and_connection_keywords:
            return new_clauses, None

        # Copy the left and right expressions and add them to the first branch
        left_exp = clause.left_expression.copy()
        right_exp = clause.right_expression.copy()
        new_clauses[0] += [left_exp]
        new_clauses[0] += [right_exp]

        # Return the branches and create the rule description
        return new_clauses, AndRule(clause, left_exp, right_exp)
