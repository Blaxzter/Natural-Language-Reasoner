from logics.Constants import connection_keywords, separator, de_morgen_expression
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize


class ConnectedExpression(Expression):
    """
    Class that represents the and / or connected expressions
    """
    def __init__(self, *args):
        # When we have only one input it must be a sentence
        if len(args) == 1:
            # Call the constructor of the Expression
            super().__init__(args[0])

            # Remove the de morgen expression and reverse the negation
            if self.tokens[0] == de_morgen_expression:
                self.negated = not self.negated
                self.tokens = self.tokens[1:]

            self.left_expression = None
            self.right_expression = None

            self.connection_keyword = None
            # Go over each connection key word
            for connection_keyword in connection_keywords:
                # Go over each word and create expression split by keyword
                if connection_keyword in self.tokens:
                    from logics.senteces.Helper import create_expression
                    keyword_idx = self.tokens.index(connection_keyword)
                    # Create the expressions from the left and right tokens
                    self.left_expression = create_expression(separator.join(self.tokens[:keyword_idx]))
                    self.right_expression = create_expression(separator.join(self.tokens[keyword_idx + 1:]))

                    self.connection_keyword = connection_keyword
                    break

            # If no keyword was found i dont know where we went wrong...
            if self.connection_keyword is None:
                raise ParseException("Connection keyword but no keyword? :thinking:")
        else:
            # Copy constructor
            self.count_id()
            self.negated = args[0]
            self.left_expression = args[1]
            self.right_expression = args[2]
            self.connection_keyword = args[3]
            self.tokenize_expression()

    def tokenize_expression(self):
        """
        Create the tokens of the expression based on detected elements
        """
        self.tokens = tokenize(
            f'{de_morgen_expression if self.negated else ""} '
            f'{self.left_expression.get_string_rep()} {self.connection_keyword} {self.right_expression.get_string_rep()}'
        )

    def replace_variable(self, replace, replace_with):
        """
        Replace the subject or object if they match the to be replaced variable
        :param replace:      To be replaced with variable
        :param replace_with: The Variable it needs to be replaced with
        :return: A new expression with the replaced variables
        """
        new_connected_expression = self.copy()
        new_connected_expression.left_expression = new_connected_expression.left_expression.replace_variable(replace, replace_with)
        new_connected_expression.right_expression = new_connected_expression.right_expression.replace_variable(replace, replace_with)
        new_connected_expression.tokenize_expression()
        return new_connected_expression

    def get_string_rep(self):
        """
        Splice expression back together with the negation word
        :return: The string representation of the expression
        """
        return f'{separator.join(self.tokens)}'

    def reverse_expression(self):
        """
        Function that flips the negated bit
        :return: The hypothesis reversed
        """
        return ConnectedExpression(
            not self.negated,
            self.left_expression,
            self.right_expression,
            self.connection_keyword
        )

    def copy(self):
        """
        Copy function that calls the copy constructor for a new clean object
        :return: The new object
        """
        return ConnectedExpression(
            self.negated,
            self.left_expression,
            self.right_expression,
            self.connection_keyword
        )