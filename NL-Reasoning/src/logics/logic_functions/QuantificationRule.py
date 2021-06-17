from collections import defaultdict

from logics.senteces.QuantifiedExpression import QuantifiedExpression
from logics.senteces.UnifiableVariable import UnifiableVariable
from logics.senteces.WhenExpression import WhenExpression
from logics.senteces.ConnectedExpression import ConnectedExpression
from logics.logic_functions.Rule import Rule
from utils.Utils import create_new_object


class QuantificationRule(Rule):

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

    def get_explanation(self, applied_rule):
        return dict(
            name=self.name,
            description=self.description,
            basic_in_expression = ["¬ for all x. P(x)" if self.negation else "¬ it exists x. P(x)"],
            basic_out_expression = [["for all x. ¬ P(x)" if not self.negation else "it exists x. ¬P(x)"]],
            in_expression=[self.expression.get_string_rep()],
            out_expression=[[self.resulting_expression.get_string_rep()]
                if type(self.resulting_expression) != list else
                [expression.get_string_rep() for expression in self.resulting_expression]],
        )

    @staticmethod
    def negation_apply_rule(clause: QuantifiedExpression, *args):
        new_clauses = defaultdict(list)
        if not clause.negated or type(clause) is not QuantifiedExpression:
            return new_clauses, None

        this_clause = clause.copy()
        this_clause.quantification_sentence = "it exists a" if this_clause.for_all else "for all"
        this_clause.for_all = not this_clause.for_all
        this_clause.quantified_expression = this_clause.quantified_expression.reverse_expression()
        return this_clause, QuantificationRule(clause, new_clauses[0])

    @staticmethod
    def apply_replace_rule(clause: QuantifiedExpression, *args):
        new_clauses = defaultdict(list)

        if clause.negated or type(clause) is not QuantifiedExpression:
            return new_clauses, None

        if clause.for_all:
            replace_with = UnifiableVariable(clause.quantified_variable)
        else:
            replace_with = create_new_object(clause.quantified_variable)

        new_clause = clause.quantified_expression.replace_variable(clause.quantified_variable, replace_with)
        new_clauses[0] += [new_clause]
        return new_clauses, QuantificationRule(clause, new_clauses[0])
