from collections import defaultdict

from logics.logic_functions.Rule import Rule
from logics.senteces.QuantifiedExpression import QuantifiedExpression
from logics.senteces.UnifiableVariable import UnifiableVariable
from utils.Utils import create_new_object


class QuantificationRule(Rule):
    """
    Class representing the application of all quantification rules
    Being the Negation rule and Replace Rule for / for all and / it exists expression
    It is required for the tool tip
    """

    def __init__(self, expression, resulting_expression, negation = False):
        self.name = 'Negation Quantification Rule' if negation else 'Quantification Replace Rule'
        self.applicable = 'Negated Quantification Rule' if negation else 'Quantification Replace Rule'
        self.negation = negation
        if negation:
            self.description = 'If we have a negated quantified expression. <br>Replace the quantifier and negate the quantified expression.'
        else:
            self.description = 'When a variable gets quantified you replace it in the quantified expression.'
        self.expression = expression
        self.resulting_expression = resulting_expression

    def get_explanation(self):
        """
        :return: Create the explanation based on the provided data in the object.
        """
        return dict(
            name = self.name,
            description = self.description,
            basic_in_expression = ["¬ for all x. P(x)" if self.negation else "any x"],
            basic_out_expression = [["for all x. ¬ P(x)" if self.negation else "c"]],
            in_expression = [self.expression.get_string_rep()],
            out_expression = [[self.resulting_expression.get_string_rep()]
                              if type(self.resulting_expression) != list else
                              [expression.get_string_rep() for expression in self.resulting_expression]],
        )

    @staticmethod
    def negation_apply_rule(clause: QuantifiedExpression, *args):
        """
        When applicable reverse the quantification and apply the negation to the expression
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """
        new_clauses = defaultdict(list)

        # Do application tests
        if not clause.negated or type(clause) is not QuantifiedExpression:
            return new_clauses, None

        # Copy the used clause and reverse the quantifier.
        this_clause = clause.copy()
        this_clause.quantification_sentence = "it exists a" if this_clause.for_all else "for all"
        this_clause.for_all = not this_clause.for_all

        # Reverese the quantified expression
        this_clause.quantified_expression = this_clause.quantified_expression.reverse_expression()

        # Return the branches and create the rule description
        return this_clause, QuantificationRule(clause, new_clauses[0], negation = True)

    @staticmethod
    def apply_replace_rule(clause: QuantifiedExpression, *args):
        """
        When applicable replace the matching variable in all expressions
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """
        new_clauses = defaultdict(list)

        # Only works on not negated expressions
        if clause.negated or type(clause) is not QuantifiedExpression:
            return new_clauses, None

        # If we have a for all quantified expression us a unification variable
        # Otherwise create a new object
        if clause.for_all:
            replace_with = UnifiableVariable(clause.quantified_variable)
        else:
            replace_with = create_new_object(clause.quantified_variable)

        # Do the recursive replace a variable call that goes through each expression
        new_clause = clause.quantified_expression.replace_variable(clause.quantified_variable, replace_with)
        new_clauses[0] += [new_clause]

        # Return the branches and create the rule description
        return new_clauses, QuantificationRule(clause, new_clauses[0], negation = False)
