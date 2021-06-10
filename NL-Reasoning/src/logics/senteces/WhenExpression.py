from logics.Constants import connection_keywords, separator, when_keywords, when_split_tokens
from logics.Expression import Expression
from utils.utils import tokenize


class WhenExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            self.when_keyword = None
            self.when_split_token = None
            split_index = -1
            # Go over each when token
            for when_token in when_keywords:

                # When the when token is in the sentence search for split token
                if when_token in self.tokens:

                    # Go over the split tokens
                    for when_split_token in when_split_tokens:
                        if when_split_token in self.tokens:
                            self.when_split_token = when_split_token
                            # get split index
                            split_index = self.tokens.index(when_split_token)
                            self.when_keyword = when_token
                            break
                    break

            if split_index == -1:
                raise Exception("No split token found: when expression require then or , keyword")

            left_tokens = list(self.tokens[:split_index])
            right_tokens = list(self.tokens[split_index + 1:])

            # Get the when expression that needs to be negated if necessary
            if self.when_keyword in left_tokens:
                when_token = left_tokens
                not_when_token = right_tokens
            else:
                when_token = right_tokens
                not_when_token = left_tokens

            when_token.remove(self.when_keyword)

            from logics.senteces.Helper import create_expression
            self.when_expression = create_expression(separator.join(when_token))
            self.not_when_expression = create_expression(separator.join(not_when_token))
        else:
            self.count_id()
            self.negated = args[0]
            self.when_expression = args[1]
            self.not_when_expression = args[2]
            self.when_keyword = args[3]
            self.when_split_token = args[4]

            self.tokens = tokenize(
                f'{"it is not the case that " if self.negated else ""}{self.when_keyword}'
                f'{self.when_expression.get_string_rep()} {self.when_split_token} {self.not_when_expression.get_string_rep()}'
            )

    def reverse_expression(self):
        return WhenExpression(
            not self.negated,
            self.when_expression,
            self.not_when_expression,
            self.when_keyword,
            self.when_split_token
        )

    def copy(self):
        return WhenExpression(
            self.negated,
            self.when_expression,
            self.not_when_token,
            self.when_keyword
        )
