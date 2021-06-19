import re

from logics.Constants import separator, syllogism_regex
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize, get_sentences_key_words


class SyllogismExpression(Expression):
    """
    Class that represents all possible syllogism expressions
    """

    def __init__(self, *args):
        # When we have only one input it must be a sentence
        if len(args) == 1:
            # Call the constructor of the Expression
            super().__init__(args[0])

            # Check for the therefore, and remove it
            if self.tokens[0] == 'therefore':
                self.tokens = self.tokens[1:]
            if self.tokens[0] == ',':
                self.tokens = self.tokens[1:]

            # The syllogism keyword
            self.syllogism_keywords = None

            # Get the string rep with the overall negation removed
            test_sentence = self.get_string_rep()
            reg_match = re.match(syllogism_regex, test_sentence, re.IGNORECASE)

            if reg_match is None:
                raise ParseException(f"No regex match found for the when expression: \n"
                                     f"Original sentence: {test_sentence}")

            # Go over each group and get the sentences between the keywords
            sentences, self.syllogism_keywords = get_sentences_key_words(reg_match, test_sentence)

            # Get the subject and object
            self.object = sentences[0]
            self.subject = sentences[1]
        else:
            # Copy constructor
            self.count_id()
            self.negated = args[0]
            self.syllogism_keywords = args[1]
            self.object = args[2]
            self.subject = args[3]

            # Re tokenize the expression
            self.tokenize_expression()

    def tokenize_expression(self):
        """
        Create the tokens of the expression based on detected elements
        """
        self.tokens = tokenize(
            f'{"it is not the case that " if self.negated else ""}'
            f'{self.syllogism_keywords[0]} {self.object} {self.syllogism_keywords[1]} {self.subject}'
        )

    def replace_variable(self, replace, replace_with):
        """
        Replace the all variables if they match the to be replaced variable
        :param replace:      To be replaced with variable
        :param replace_with: The Variable it needs to be replaced with
        :return: A new expression with the replaced variables
        """
        new_syllogism_exp = self.copy()
        if new_syllogism_exp.object == replace:
            new_syllogism_exp.object = replace_with
        if new_syllogism_exp.subject == replace:
            new_syllogism_exp.subject = replace_with
        new_syllogism_exp.tokenize_expression()
        return new_syllogism_exp

    def reverse_expression(self):
        """
        Function that flips the negated bit
        :return: The hypothesis reversed
        """
        return SyllogismExpression(
            not self.negated,
            self.syllogism_keywords,
            self.object,
            self.subject
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
        return SyllogismExpression(
            self.negated,
            self.syllogism_keywords,
            self.object,
            self.subject
        )
