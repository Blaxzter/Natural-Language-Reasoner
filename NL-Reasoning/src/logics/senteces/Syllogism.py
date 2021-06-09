from logics.Expression import Expression


class SyllogismExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            # Check for syllogisms
            if self.tokens[0] == 'therefore':
                self.tokens = self.tokens[2:]
                self.is_syllogism = True
        else:
            self.count_id()

    def reverse_expression(self):
        pass

    def copy(self):
        pass