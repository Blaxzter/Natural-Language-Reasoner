import re

from logics.Constants import separator, quantified_regex_plural, quantified_regex_singular
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize, get_sentences_key_words


class QuantifiedExpression(Expression):
    """
    The quantified expression represent the for all or it exisits expression
    """

    def __init__(self, *args):
        # When we have only one input it must be a sentence
        if len(args) == 1:
            # Call the constructor of the Expression
            super().__init__(args[0])

            # Create expected variables
            self.for_all = True
            self.quantification_sentence = None
            self.quantified_variable = None
            self.quantified_expression = None

            # Get the string rep with the overall negation removed
            test_sentence = self.get_string_rep()

            # Get whether it is for all or it exists quantified
            reg_match = None
            for test_reg, for_all in [(quantified_regex_plural, True), (quantified_regex_singular, False)]:
                reg_match = re.match(test_reg, test_sentence, re.IGNORECASE)
                if reg_match:
                    self.for_all = for_all
                    break

            # If we have no match return false.. What ever happend here
            if reg_match is None:
                raise ParseException(f"No regex match found for the quantified expression: \n"
                                     f"Original sentence: {test_sentence}")

            # Go over each group and get the sentences between the keywords
            sentences, key_words = get_sentences_key_words(reg_match, test_sentence)

            # Get the respective data
            self.quantification_sentence = key_words[0]
            self.quantification_split = key_words[1]
            self.quantified_variable = sentences[0]

            # Create the remaining expression
            from logics.senteces.Helper import create_expression
            self.quantified_expression = create_expression(sentences[1])
        else:
            # Copy constructor
            self.count_id()

            self.negated = args[0]
            self.for_all = args[1]
            self.quantification_sentence = args[2]
            self.quantification_split = args[3]
            self.quantified_variable = args[4]
            self.quantified_expression = args[5]

        # Re tokenize the expression
        self.tokenize_expression()

    def tokenize_expression(self):
        """
        Create the tokens of the expression based on detected elements
        """
        self.tokens = tokenize(
            f'{"it is not the case that " if self.negated else ""}'
            f'{self.quantification_sentence} {self.quantified_variable} {self.quantification_split} {self.quantified_expression.get_string_rep()}'
        )

    def replace_variable(self, replace, replace_with):
        """
        Replace the all variables if they match the to be replaced variable
        :param replace:      To be replaced with variable
        :param replace_with: The Variable it needs to be replaced with
        :return: A new expression with the replaced variables
        """
        new_quantified_expression = self.copy()
        if new_quantified_expression.quantified_variable == replace:
            new_quantified_expression.quantified_variable = replace_with
        new_quantified_expression.quantified_expression = new_quantified_expression.quantified_expression.replace_variable(
            replace, replace_with)
        new_quantified_expression.tokenize_expression()
        return new_quantified_expression

    def reverse_expression(self):
        """
        Function that flips the negated bit
        :return: The hypothesis reversed
        """
        return QuantifiedExpression(
            not self.negated,
            self.for_all,
            self.quantification_sentence,
            self.quantification_split,
            self.quantified_variable,
            self.quantified_expression
        )

    def get_string_rep(self):
        """
        Just joins the tokens using the separator
        :return: The string representation of the expression
        """
        return f'{separator.join(self.tokens)}'

    def copy(self):
        """
        Copy function that calls the copy constructor for a new clean object
        :return: The new object
        """
        return QuantifiedExpression(
            self.negated,
            self.for_all,
            self.quantification_sentence,
            self.quantification_split,
            self.quantified_variable,
            self.quantified_expression
        )
