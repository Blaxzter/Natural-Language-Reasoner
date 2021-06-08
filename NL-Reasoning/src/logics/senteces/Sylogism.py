from logics.Expression import Expression


class Syllogism(Expression):

    def __init__(self, hypothesis):
        super().__init__(hypothesis)

        # Check for syllogisms
        if self.tokens[0] == 'therefore':
            self.tokens = self.tokens[2:]
            self.is_syllogism = True