from logics.Constants import connection_keywords, separator, de_morgen_expression
from logics.senteces.Expression import Expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize


class ConnectedExpression(Expression):

    def __init__(self, *args):

        if len(args) == 1:
            super().__init__(args[0])

            if self.tokens[0] == de_morgen_expression:
                self.negated = not self.negated
                self.tokens = self.tokens[1:]

            self.left_expression = None
            self.right_expression = None

            self.connection_keyword = None
            for connection_keyword in connection_keywords:
                # Go over each word and create expression split by keyword
                if connection_keyword in self.tokens:
                    from logics.senteces.Helper import create_expression
                    keyword_idx = self.tokens.index(connection_keyword)
                    self.left_expression = create_expression(separator.join(self.tokens[:keyword_idx]))
                    self.right_expression = create_expression(separator.join(self.tokens[keyword_idx + 1:]))

                    self.connection_keyword = connection_keyword
                    break

            if self.connection_keyword is None:
                raise ParseException("Connection keyword but no keyword? :thinking:")
        else:
            self.count_id()
            self.negated = args[0]
            self.left_expression = args[1]
            self.right_expression = args[2]
            self.connection_keyword = args[3]
            self.tokenize_expression()

    def tokenize_expression(self):
        self.tokens = tokenize(
            f'{de_morgen_expression if self.negated else ""}'
            f'{self.left_expression.get_string_rep()} {self.connection_keyword} {self.right_expression.get_string_rep()}'
        )

    def replace_variable(self, replace, replace_with):
        new_connected_expression = self.copy()
        new_connected_expression.left_expression = new_connected_expression.left_expression.replace_variable(replace, replace_with)
        new_connected_expression.right_expression = new_connected_expression.right_expression.replace_variable(replace, replace_with)
        new_connected_expression.tokenize_expression()
        return new_connected_expression

    def get_string_rep(self):
        return f'{"neither " if self.negated else ""}{separator.join(self.tokens)}'

    def reverse_expression(self):
        return ConnectedExpression(
            not self.negated,
            self.left_expression,
            self.right_expression,
            self.connection_keyword
        )

    def copy(self):
        return ConnectedExpression(
            self.negated,
            self.left_expression,
            self.right_expression,
            self.connection_keyword
        )

class ConnectedExpressionGrouped(Expression):

    def __init__(self, hypothesis):
        super().__init__(hypothesis)

        expression_groups = []

        self.connection_keyword = None
        for connection_keyword in connection_keywords:

            # Go over each word and create expression split by keyword
            if connection_keyword in self.tokens:
                from logics.senteces.Helper import create_expression
                start_idx = 0
                for idx, token in enumerate(self.tokens):
                    if token == connection_keyword:
                        current_part = self.tokens[start_idx:idx]
                        expression_groups.append(create_expression(separator.join(current_part)))
                        start_idx = idx + 1

                if start_idx < len(self.tokens):
                    current_part = self.tokens[start_idx:len(self.tokens)]
                    expression_groups.append(create_expression(separator.join(current_part)))

                self.connection_keyword = connection_keyword
                break

        if self.connection_keyword is None:
            raise Exception("Connection keyword but no keyword? :thinking:")
