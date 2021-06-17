import re

from logics.Constants import separator, quantified_keywords_plural, quantified_keywords_singular, \
    quantified_regex_plural, quantified_regex_singular
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize, get_sentences_key_words


class QuantifiedExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            self.for_all = True
            self.quantification_sentence = None
            self.quantified_variable = None
            self.quantified_expression = None

            test_sentence = self.get_string_rep()

            reg_match = None
            for test_reg, for_all in [(quantified_regex_plural, True), (quantified_regex_singular, False)]:
                reg_match = re.match(test_reg, test_sentence, re.IGNORECASE)
                if reg_match:
                    self.for_all = for_all
                    break

            if reg_match is None:
                raise ParseException(f"No regex match found for the quantified expression: \n"
                                     f"Original sentence: {test_sentence}")

            # Go over each group and get the sentences between the keywords
            sentences, key_words = get_sentences_key_words(reg_match, test_sentence)

            self.quantification_sentence = key_words[0]
            self.quantification_split = key_words[1]

            self.quantified_variable = sentences[0]

            from logics.senteces.Helper import create_expression
            self.quantified_expression = create_expression(sentences[1])
        else:
            self.count_id()

            self.negated = args[0]
            self.for_all = args[1]
            self.quantification_sentence = args[2]
            self.quantification_split = args[3]
            self.quantified_variable = args[4]
            self.quantified_expression = args[5]

        self.tokenize_expression()

    def tokenize_expression(self):
        self.tokens = tokenize(
            f'{"it is not the case that " if self.negated else ""}'
            f'{self.quantification_sentence} {self.quantified_variable} {self.quantification_split} {self.quantified_expression.get_string_rep()}'
        )

    def replace_variable(self, replace, replace_with):
        new_quantified_expression = self.copy()
        if new_quantified_expression.quantified_variable == replace:
            new_quantified_expression.quantified_variable = replace_with
        new_quantified_expression.quantified_expression = new_quantified_expression.quantified_expression.replace_variable(replace, replace_with)
        new_quantified_expression.tokenize_expression()
        return new_quantified_expression

    def reverse_expression(self):
        return QuantifiedExpression(
            not self.negated,
            self.for_all,
            self.quantification_sentence,
            self.quantification_split,
            self.quantified_variable,
            self.quantified_expression
        )

    def get_string_rep(self):
        return f'{separator.join(self.tokens)}'

    def copy(self):
        return QuantifiedExpression(
            self.negated,
            self.for_all,
            self.quantification_sentence,
            self.quantification_split,
            self.quantified_variable,
            self.quantified_expression
        )
