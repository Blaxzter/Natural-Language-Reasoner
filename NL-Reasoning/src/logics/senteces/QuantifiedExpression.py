from logics.Constants import separator, quantified_keywords_plural, quantified_keywords_singular
from logics.senteces.Expression import Expression
from utils.utils import tokenize


class QuantifiedExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            self.for_all = True
            self.quantified_sentence = None
            self.quantified_variable = None
            self.quantified_expression = None

            for quantified_keyword_singular in quantified_keywords_singular:
                if quantified_keyword_singular in self.init_hypo:
                    self.for_all = False
                    self.quantified_sentence = tokenize(quantified_keyword_singular)

            if self.quantified_sentence is None:
                for quantified_keyword_plural in quantified_keywords_plural:
                    if quantified_keyword_plural in self.init_hypo:
                        self.quantified_sentence = tokenize(quantified_keyword_plural)

            quantified_token_length = len(self.quantified_sentence)
            self.quantified_variable = self.tokens[quantified_token_length + 1]
            from logics.senteces.Helper import create_expression
            self.quantified_expression = create_expression(separator.join(self.tokens[quantified_token_length + 1:]))

        else:
            self.count_id()

            self.for_all = args[0]
            self.quantified_sentence = args[1]
            self.quantified_variable = args[2]
            self.quantified_expression = args[3]

            self.tokens = tokenize(
                f'{self.quantified_sentence} {self.quantified_variable} {self.quantified_expression}'
            )

    def reverse_expression(self):
        return QuantifiedExpression(
            not self.negated,
            self.for_all,
            self.quantified_sentence,
            self.quantified_variable,
            self.quantified_expression
        )

    def get_string_rep(self):
        return f'{"it is not the case that " if self.negated else ""}{separator.join(self.tokens)}'

    def copy(self):
        return QuantifiedExpression(
            self.negated,
            self.for_all,
            self.quantified_sentence,
            self.quantified_variable,
            self.quantified_expression
        )
