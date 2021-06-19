from typing import List

from logics.Constants import connection_keywords, complete_negation, separator, de_morgen_expression
from logics.senteces.ParseExceptions import ParseException
from utils.Utils import tokenize
import abc


class Expression(metaclass=abc.ABCMeta):
    """
    Expression that is a abstract class of which each expression has to be parent of
    """
    id_counter = 0      # The expression counter for each new expression

    def __init__(self, hypothesis):
        # We just want strings or lists (tokens) nothing else
        if hypothesis is None or (type(hypothesis) is not str and type(hypothesis) is not list):
            raise ParseException("A hypothesis needs to be of type string or token list and can't be empty.")

        # Get the new id
        self.count_id()

        if type(hypothesis) is str:
            self.init_hypo = hypothesis.lower()  # Only use lower case
            self.tokens: List = tokenize(self.init_hypo)  # Split hypo into tokens
        else:
            self.init_hypo = " ".join(hypothesis)
            self.tokens = hypothesis

        # If the "It is not the case that ..." is used remove it from the tokens
        self.negated = False
        if complete_negation in self.init_hypo:
            self.negated = True
            self.tokens = self.tokens[6:]

        # Get the a plays b or c -> a plays b or a plays c
        self.split_references()

    def count_id(self):
        """
        Creat a new id
        """
        self.id = Expression.id_counter
        Expression.id_counter += 1

    def split_references(self):
        """
        Splits the sentence that references previous subjects into multiple base tokens
        """
        for reference in connection_keywords:
            if reference in self.tokens:
                reference_idx = self.tokens.index(reference)
                right_tokens = self.tokens[reference_idx + 1:]

                # If the right sentence is not just one word we dont support that atm
                if len(right_tokens) != 1:
                    continue

                start_idx = 1 if self.tokens[0] == de_morgen_expression else 0
                base_tokens = self.tokens[start_idx:reference_idx - 1]
                left_tokens = self.tokens[:reference_idx]

                self.tokens = left_tokens + [reference] + base_tokens + right_tokens

    def is_tautologie_of(self, clause, list_of_new_objects):
        return False

    @abc.abstractmethod
    def reverse_expression(self):
        pass

    @abc.abstractmethod
    def replace_variable(self, replace, replace_with):
        pass

    @abc.abstractmethod
    def copy(self):
        pass

    def contains(self, word):
        if word in self.tokens:
            return True
        else:
            return False

    def get_string_rep(self):
        return separator.join(self.tokens)

    def __str__(self):
        return f'{type(self).__name__}(neg={self.negated}, tokens={self.tokens})'

    def __repr__(self):
        return f'{self.tokens}'

    def __len__(self):
        return len(self.tokens)