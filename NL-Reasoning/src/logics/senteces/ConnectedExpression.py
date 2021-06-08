from logics.Constants import connection_keywords, separator
from logics.Expression import Expression
from logics.senteces.Helper import create_expression


class ConnectedExpression(Expression):

    def __init__(self, hypothesis):
        super().__init__(hypothesis)

        expression_groups = []

        self.connection_keyword = None
        for connection_keyword in connection_keywords:

            # Go over each word and create expression split by keyword
            if connection_keyword in self.tokens:
                start_idx = 0
                for idx, token in enumerate(self.tokens):
                    if token == connection_keyword:
                        current_part = self.tokens[start_idx:idx]
                        expression_groups.append(create_expression(separator.join(current_part)))
                self.connection_keyword = connection_keyword
                break

        if self.connection_keyword is None:
            raise Exception("Connection keyword but no keyword? :thinking:")



