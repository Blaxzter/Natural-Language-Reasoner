import re

from logics.Constants import when_left_regex, when_right_regex
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize, get_sentences_key_words


class WhenExpression(Expression):
    """
    Class representing the "when Expression then Expression" sentence
    """

    def __init__(self, *args):
        # When we have only one input it must be a sentence
        if len(args) == 1:
            # Call the constructor of the Expression
            super().__init__(args[0])

            # Get the string rep with the overall negation removed
            test_sentence = self.get_string_rep()

            self.left_match = None
            self.key_words = None

            # Check whether we have a left when expression or right when expression
            reg_match = None
            for test_reg, is_left in [(when_left_regex, True), (when_right_regex, False)]:
                reg_match = re.match(test_reg, test_sentence, re.IGNORECASE)
                if reg_match:
                    self.left_match = is_left
                    break

            if reg_match is None:
                raise ParseException(f"No regex match found for the when expression: \n"
                                     f"Original sentence: {test_sentence}")

            # Go over each group and get the sentences between the keywords
            sentences, self.key_words = get_sentences_key_words(reg_match, test_sentence)

            if len(sentences) != 2:
                raise ParseException(f"The when expression doesn't have two sentences"
                                     f"Original sentence: {test_sentence}")

            # Get the when expression that needs to be negated if necessary
            from logics.senteces.Helper import create_expression
            if self.left_match:
                self.when_expression = create_expression(sentences[0])
                self.not_when_expression = create_expression(sentences[1])
            else:
                self.when_expression = create_expression(sentences[1])
                self.not_when_expression = create_expression(sentences[0])

        else:
            # Copy constructor
            self.count_id()
            self.negated = args[0]
            self.when_expression = args[1]
            self.not_when_expression = args[2]
            self.left_match = args[3]
            self.key_words = args[4]
            self.tokenize_expression()

    def tokenize_expression(self):
        """
        Create the tokens of the expression based on detected elements
        """
        sentence = f'{"it is not the case that " if self.negated else ""}'
        sentence += \
            f'{self.key_words[0]} {self.when_expression.get_string_rep()} {self.key_words[1]} {self.not_when_expression.get_string_rep()}' \
                if self.left_match else \
                f'{self.not_when_expression.get_string_rep()} {self.key_words[0]} {self.when_expression.get_string_rep()}'

        self.tokens = tokenize(sentence)

    def replace_variable(self, replace, replace_with):
        """
        Replace the all variables if they match the to be replaced variable
        :param replace:      To be replaced with variable
        :param replace_with: The Variable it needs to be replaced with
        :return: A new expression with the replaced variables
        """
        new_when_expression = self.copy()
        new_when_expression.when_expression = new_when_expression.when_expression.replace_variable(replace,
                                                                                                   replace_with)
        new_when_expression.not_when_expression = new_when_expression.not_when_expression.replace_variable(replace,
                                                                                                           replace_with)
        new_when_expression.tokenize_expression()
        return new_when_expression

    def reverse_expression(self):
        """
        Function that flips the negated bit
        :return: The hypothesis reversed
        """
        return WhenExpression(
            not self.negated,
            self.when_expression,
            self.not_when_expression,
            self.left_match,
            self.key_words
        )

    def copy(self):
        """
        Copy function that calls the copy constructor for a new clean object
        :return: The new object
        """
        return WhenExpression(
            self.negated,
            self.when_expression,
            self.not_when_expression,
            self.left_match,
            self.key_words
        )
