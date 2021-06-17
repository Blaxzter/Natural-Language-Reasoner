import re

from logics.Constants import separator, quantified_keywords_plural, quantified_keywords_singular, multi_function_regex, \
    single_function_regex, neg_function_keywords, get_opposite_of_function, pos_function_keywords
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from logics.senteces.UnifiableVariable import UnifiableVariable
from utils.Utils import tokenize, get_sentences_key_words, list_in_check, create_new_object


class FunctionExpression(Expression):
    """
    This class holds the function expressions

    The function expression considers compared to the base expression that something is something.
    A is a X or A is a X of B for the multi function option.
    """

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

            self.check_negation(key_words)

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

    def check_negation(self, key_words):

        neg_list_check = list_in_check(neg_function_keywords, key_words)
        if neg_list_check is not None:
            if self.negated:
                self.negated = False
                key_words[0] = get_opposite_of_function(key_words[0])
            else:
                self.negated = True
        else:
            if self.negated:
                key_words[0] = get_opposite_of_function(key_words[0])

    def tokenize_expression(self):
        sentence = \
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

    def is_tautologie_of(self, clause, list_of_new_objects):
        if self.negated == clause.negated:
            return False, None

        unification_replacements = []

        for i, variable in enumerate(self.variables):

            comp_variable = clause.variables[i]
            if type(variable) == UnifiableVariable:
                if type(comp_variable) == UnifiableVariable:
                    # Both are unifiable Variables
                    new_object = create_new_object(list_of_new_objects)
                    unification_replacements.append((new_object, variable))
                    unification_replacements.append((new_object, comp_variable))
                else:
                    unification_replacements.append((comp_variable, variable))
            elif type(comp_variable) == UnifiableVariable:
                unification_replacements.append((variable, comp_variable))
            elif variable != clause.variables[i]:
                return False, None

        return self.quantified_function == clause.quantified_function, unification_replacements

    def reverse_expression(self):

        opposite_keyword = get_opposite_of_function(self.key_words[0])

        return FunctionExpression(
            not self.negated,
            self.variables,
            self.quantified_function,
            [opposite_keyword] + self.key_words[1:],
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
