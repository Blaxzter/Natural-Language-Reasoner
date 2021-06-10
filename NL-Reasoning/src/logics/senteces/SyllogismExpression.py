from logics.Constants import pluralism_keywords, separator
from logics.Expression import Expression
from utils.utils import tokenize


class SyllogismExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            # Check for syllogisms
            if self.tokens[0] == 'therefore':
                self.tokens = self.tokens[2:]

            self.is_individual = True
            self.syllogism_keyword = None

            for pluralism_keyword in pluralism_keywords:
                if pluralism_keyword in self.tokens:
                    self.is_individual = False
                    self.syllogism_keyword = (pluralism_keyword, self.tokens[2:-1])
                    break

            self.individual_keyword = None
            if self.syllogism_keyword is None:
                self.individual_keyword = self.tokens[1:-1]

            # Get the subject and object
            self.object = self.tokens[0 if self.is_individual else 1]
            self.subject = self.tokens[-1]
        else:
            self.count_id()
            self.negated = args[0]
            self.is_individual = args[1]

            self.syllogism_keyword = None
            self.individual_keyword = None

            if self.is_individual:
                self.individual_keyword = args[2]
            else:
                self.syllogism_keyword = args[2]

            self.object = args[3]
            self.subject = args[4]

            self.tokens = tokenize(
                f'{self.object} {separator.join(self.individual_keyword)} {self.subject}'
                if self.is_individual else
                f'{self.syllogism_keyword[0]} {self.object} {separator.join(self.syllogism_keyword[1])} {self.subject}'
            )

    def reverse_expression(self):
        return SyllogismExpression(
            not self.negated,
            self.is_individual,
            self.individual_keyword if self.is_individual else self.syllogism_keyword,
            self.object,
            self.subject
        )

    def get_string_rep(self):
        return f'{"it is not the case that " if self.negated else ""}{separator.join(self.tokens)}'

    def copy(self):
        return SyllogismExpression(
            self.negated,
            self.is_individual,
            self.individual_keyword if self.is_individual else self.syllogism_keyword,
            self.object,
            self.subject
        )
