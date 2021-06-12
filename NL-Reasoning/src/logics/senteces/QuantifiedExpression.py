from logics.Constants import pluralism_keywords, separator
from logics.Expression import Expression
from utils.utils import tokenize


class PredicateExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            self.for_all = True
            self.quantified_sentence = None
            self.quantified_variable = None
            self.quantified_expression = None


        else:
            self.count_id()

            self.for_all = args[0]
            self.quantified_sentence = args[1]
            self.quantified_variable = args[2]
            self.quantified_expression = args[3]

            self.tokens = tokenize(
                f'{self.quantified_sentence} {separator.join(self.individual_keyword)} {self.subject}'
                if self.for_all else
                f'{self.syllogism_keyword[0]} {self.object} {separator.join(self.syllogism_keyword[1])} {self.subject}'
            )

    def reverse_expression(self):
        return PredicateExpression(
            not self.negated,
            self.is_individual,
            self.individual_keyword if self.is_individual else self.syllogism_keyword,
            self.object,
            self.subject
        )

    def get_string_rep(self):
        return f'{"it is not the case that " if self.negated else ""}{separator.join(self.tokens)}'

    def copy(self):
        return PredicateExpression(
            self.negated,
            self.is_individual,
            self.individual_keyword if self.is_individual else self.syllogism_keyword,
            self.object,
            self.subject
        )
