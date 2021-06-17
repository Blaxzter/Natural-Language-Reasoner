import re

from logics.Constants import pluralism_keywords, separator, syllogism_regex
from logics.senteces.Expression import Expression
from logics.senteces.ParseException import ParseException
from utils.Utils import tokenize, get_sentences_key_words


class SyllogismExpression(Expression):

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])

            # Check for syllogisms
            if self.tokens[0] == 'therefore':
                self.tokens = self.tokens[2:]

            self.syllogism_keywords = None

            test_sentence = self.get_string_rep()
            reg_match = re.match(syllogism_regex, test_sentence, re.IGNORECASE)

            if reg_match is None:
                raise ParseException(f"No regex match found for the when expression: \n"
                                     f"Original sentence: {test_sentence}")

            # Go over each group and get the sentences between the keywords
            sentences, self.syllogism_keywords = get_sentences_key_words(reg_match, test_sentence)

            # Get the subject and object
            self.object = sentences[0]
            self.subject = sentences[1]
        else:
            self.count_id()
            self.negated = args[0]
            self.syllogism_keywords = args[1]
            self.object = args[2]
            self.subject = args[3]

            self.tokenize_expression()

    def tokenize_expression(self):
        self.tokens = tokenize(
            f'{"it is not the case that " if self.negated else ""}'
            f'{self.syllogism_keywords[0]} {self.object} {self.syllogism_keywords[1]} {self.subject}'
        )

    def replace_variable(self, replace, replace_with):
        new_syllogism_exp = self.copy()
        if new_syllogism_exp.object == replace:
            new_syllogism_exp.object = replace_with
        if new_syllogism_exp.subject == replace:
            new_syllogism_exp.subject = replace_with
        new_syllogism_exp.tokenize_expression()
        return new_syllogism_exp

    def reverse_expression(self):
        return SyllogismExpression(
            not self.negated,
            self.syllogism_keywords,
            self.object,
            self.subject
        )

    def get_string_rep(self):
        return f'{separator.join(self.tokens)}'

    def copy(self):
        return SyllogismExpression(
            self.negated,
            self.syllogism_keywords,
            self.object,
            self.subject
        )
