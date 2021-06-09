from typing import List

from logics.Constants import connection_keywords, complete_negation, separator
from utils.utils import tokenize
import abc


class Expression(metaclass=abc.ABCMeta):
    id_counter = 0

    def __init__(self, hypothesis):

        if hypothesis is None or (type(hypothesis) is not str and type(hypothesis) is not list):
            raise ValueError("A hypothesis needs to be of type string or token list and can't be empty.")

        self.count_id()

        if type(hypothesis) is str:
            self.init_hypo = hypothesis.lower()  # Only use lower case
            self.tokens: List = tokenize(self.init_hypo)  # Split hypo into tokens
        else:
            self.init_hypo = " ".join(hypothesis)
            self.tokens = hypothesis

        self.negated = False
        if complete_negation in self.init_hypo:
            self.negated = True
            self.tokens = self.tokens[6:]

        self.split_references()

    def count_id(self):
        self.id = Expression.id_counter
        Expression.id_counter += 1

    def split_references(self):
        """
        Splits the sentence that references previous subjects into multiple base tokens
        TODO Should probably be rewritten to check if separated by semicolon
        :return:
        """
        for reference in connection_keywords:
            if reference in self.tokens:
                reference_idx = self.tokens.index(reference)
                right_tokens = self.tokens[reference_idx + 1:]

                # If the right sentence is not just one word we dont support that atm
                if len(right_tokens) != 1:
                    continue

                base_tokens = self.tokens[:reference_idx - 1]
                left_tokens = self.tokens[:reference_idx]

                self.tokens = left_tokens + [reference] + base_tokens + right_tokens

    @abc.abstractmethod
    def reverse_expression(self):
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
        return str(self.tokens)

    def __repr__(self):
        return f'{self.tokens}'

    def __len__(self):
        return len(self.tokens)