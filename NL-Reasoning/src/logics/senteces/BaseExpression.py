from logics.Constants import negation_keywords
from logics.Expression import Expression


class BaseExpression(Expression):

    def __init__(self, hypothesis):
        # Call the constructor of the Expression
        super().__init__(hypothesis)

        # Get whether the sentence is negated
        self.negated = False
        self.negation_word = 'not'
        for negation_keyword in negation_keywords:
            if negation_keyword in self.tokens:
                self.negated = True
                self.negation_word = negation_keyword
                break

        self.tokens.remove(self.negation_word)
        self.subject = self.tokens[0]
        self.verb = self.tokens[1]
        self.object = self.tokens[2]

    def reverse_expression(self):
        """
        Function that flips the negated bit
        :return: The hypothesis reversed
        """
        self.negated = not self.negated

    def is_tautologie_of(self, clause):

        if type(clause) is not BaseExpression:
            return False

        if clause.negated == self.negated:
            return False

        return self.object == clause.object and \
            self.verb == clause.verb and \
            self.subject == clause.subject

    def is_applicable(self, param):
        return False

    def get_string_rep(self):
        """
        Splice the subject, verb and object together with the negation word
        :return:
        """
        return f'{self.subject} {self.verb}{" " + self.negation_word + " " if self.negated else " "}{self.object}'
