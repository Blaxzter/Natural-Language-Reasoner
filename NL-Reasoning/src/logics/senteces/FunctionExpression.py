import re

from logics.Constants import separator, quantified_keywords_plural, quantified_keywords_singular, multi_function_regex, \
    single_function_regex
from logics.senteces.Expression import Expression
from logics.senteces.ParseException import ParseException
from utils.Utils import tokenize, get_sentences_key_words


class FunctionExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            self.variables = []
            self.quantified_function = None
            self.key_words = None
            self.multi = None

            test_sentence = self.get_string_rep()

            reg_match = None
            for test_reg, multi in [(multi_function_regex, True), (single_function_regex, False)]:
                reg_match = re.match(test_reg, test_sentence, re.IGNORECASE)
                if reg_match:
                    self.multi = multi
                    break

            if reg_match is None:
                raise ParseException(f"No regex match found for the function expression: \n"
                                     f"Original sentence: {test_sentence}")

            variables, key_words = get_sentences_key_words(reg_match, test_sentence)

            if variables[0] == 'it':
                raise ParseException(f"It is not valid as a variable.")

            self.variables = [variables[0]] if not self.multi else [variables[0], variables[-1]]
            self.quantified_function = variables[1]
            self.key_words = key_words
        else:
            self.count_id()

            self.negated = args[0]
            self.variables = args[1]
            self.quantified_function = args[2]
            self.key_words = args[3]
            self.multi = args[4]

        self.tokenize_expression()

    def tokenize_expression(self):
        sentence = f'{"it is not the case that " if self.negated else ""}'
        sentence += \
            f'{self.variables[0]} {self.key_words[0]} {self.quantified_function} {self.key_words[1]} {self.variables[1]}' \
                if self.multi else \
                f'{self.variables[0]} {self.key_words[0]} {self.quantified_function}'
        self.tokens = tokenize(sentence)

    def replace_variable(self, replace, replace_with):
        new_function_expression = self.copy()
        for i, variable in enumerate(new_function_expression.variables):
            if variable == replace:
                new_function_expression.variables[i] = replace_with
        new_function_expression.tokenize_expression()
        return new_function_expression

    def is_tautologie_of(self, clause):
        if 'not' in self.key_words[0] and 'not' in clause.key_words[0]:
            return False

        if 'not' not in self.key_words[0] and 'not' not in clause.key_words[0]:
            return False

        for i, variable in enumerate(self.variables):
            if variable != clause.variables[i]:
                return False

        return self.quantified_function == clause.quantified_function

    def reverse_expression(self):
        return FunctionExpression(
            not self.negated,
            self.variables,
            self.quantified_function,
            self.key_words,
            self.multi
        )

    def get_string_rep(self):
        return f'{separator.join(self.tokens)}'

    def copy(self):
        return FunctionExpression(
            self.negated,
            self.variables,
            self.quantified_function,
            self.key_words,
            self.multi
        )
