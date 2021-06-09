from logics.Constants import negation_keywords
from logics.Expression import Expression
from utils.utils import tokenize


class BaseExpression(Expression):

    def __init__(self, *args):

        if len(args) == 1:

            # Call the constructor of the Expression
            super().__init__(args[0])

            # Get whether the sentence is negated
            self.negation_word = 'not'
            for negation_keyword in negation_keywords:
                if negation_keyword in self.tokens:
                    self.negated = True
                    self.negation_word = negation_keyword
                    break

            if self.negated:
                self.tokens.remove(self.negation_word)
            self.subject = self.tokens[0]
            self.verb = self.tokens[1]
            self.object = self.tokens[2]
        else:
            self.count_id()
            self.negated = args[0]
            self.negation_word = args[1]
            self.subject = args[2]
            self.verb = args[3]
            self.object = args[4]

            self.tokens = tokenize(
                f'{self.subject} {self.verb}{" " + self.negation_word + " " if self.negated else " "}{self.object}'
            )

    def reverse_expression(self):
        """
        Function that flips the negated bit
        :return: The hypothesis reversed
        """
        return BaseExpression(
            not self.negated,
            self.negation_word,
            self.subject,
            self.verb,
            self.object
        )

    def is_tautologie_of(self, clause):

        if type(clause) is not BaseExpression:
            return False

        if clause.negated == self.negated:
            return False

        return self.object == clause.object and \
            self.verb == clause.verb and \
            self.subject == clause.subject

    def get_string_rep(self):
        """
        Splice the subject, verb and object together with the negation word
        :return:
        """
        return f'{self.subject} {self.verb}{" " + self.negation_word + " " if self.negated else " "}{self.object}'

    def copy(self):
        return BaseExpression(
            self.negated,
            self.negation_word,
            self.subject,
            self.verb,
            self.object
        )
