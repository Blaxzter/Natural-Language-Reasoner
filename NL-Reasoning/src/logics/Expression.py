from typing import List

from logics.Constants import connection_keywords
from utils.utils import tokenize, detect_sentence_structure


class Expression:
    id_counter = 0

    def __init__(self, hypothesis):

        if hypothesis is None or (type(hypothesis) is not str and type(hypothesis) is not list):
            raise ValueError("A hypothesis needs to be of type string or token list and can't be empty.")

        self.id = Expression.id_counter
        Expression.id_counter += 1

        if type(hypothesis) is str:
            self.init_hypo = hypothesis.lower()  # Only use lower case
            self.tokens: List = tokenize(self.init_hypo)  # Split hypo into tokens
        else:
            self.init_hypo = " ".join(hypothesis)
            self.tokens = hypothesis

        self.split_references()

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

    def get_string_rep(self):
        return self.init_hypo

    def __str__(self):
        return str(self.tokens)

    def __repr__(self):
        return f'{self.tokens}'

    def __len__(self):
        return len(self.tokens)

    def is_applicable(self, param):
        # Simple structure expected for now explanation further down for now just a in check
        # TODO more elaborate // Add hierarchical structure

        if self.is_base_expression:
            return False
        if param == 'deMorgan':
            if self.contains('!') and self.contains('('):
                return True

        return param in self.tokens

    def get_applicable_token(self, split_token):
        # Simple structure expected for now explanation further down for now just a in check
        # TODO more elaborate // Add hierarchical structure
        if split_token == 'and' or split_token == 'or':
            return self.tokens.index(split_token)
        elif split_token == 'when' or split_token == 'if':
            # Probably dont want to support hierarchical structures with when expression
            return self.tokens.index(',')
        elif split_token == 'DeMorgan':
            return self.tokens.index('!(')

        raise NotImplementedError("The rule has not been implemented yet.")

    def contains(self, word):
        if word in self.tokens:
            return True
        else:
            return False
