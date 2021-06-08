from logics.Constants import connection_keywords, separator, when_keywords, when_split_tokens
from logics.Expression import Expression
from logics.senteces.Helper import create_expression


class WhenExpression(Expression):

    def __init__(self, hypothesis):
        super().__init__(hypothesis)

        when_keyword = None
        split_index = -1
        # Go over each when token
        for when_token in when_keywords:

            # When the when token is in the sentence search for split token
            if when_token in self.tokens:

                # Go over the split tokens
                for when_split_token in when_split_tokens:
                    # get split index
                    split_index = self.tokens.index(when_split_token)
                    when_keyword = when_token
                break

        if split_index == -1:
            raise Exception("No split token found: when expression require then or , keyword")

        left_tokens = list(self.tokens[:split_index])
        right_tokens = list(self.tokens[split_index + 1:])

        # Get the when expression that needs to be negated if nessesarry
        if when_keyword in left_tokens:
            self.when_token = left_tokens
            self.not_when_token = right_tokens
        else:
            self.when_token = right_tokens
            self.not_when_token = left_tokens

        self.when_token.remove(when_keyword)

        self.when_expression = create_expression(separator.join(self.when_token))
        self.not_when_token = create_expression(separator.join(self.when_token))
