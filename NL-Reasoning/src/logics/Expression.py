from typing import List

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

        self.is_syllogism = False

        # A base expression has a few cases
        self.is_base_expression = False

        # Check for syllogisms
        if self.tokens[0] == 'therefore':
            self.tokens = self.tokens[2:]
            self.is_syllogism = True


        # Simple test if we have 3 or 4 (in not case) tokens then it is a base expression
        if len(self) == 3 or len(self) == 4:
            self.is_base_expression = True

    def split_references(self):
        """
        Splits the sentence that references previous subjects into multiple base tokens
        TODO Should probably be rewritten to check if separated by semicolon
        :return:
        """
        for reference in ['or', 'and']:
            if reference in self.tokens:
                reference_idx = self.tokens.index(reference)
                right_tokens = self.tokens[reference_idx + 1:]

                # If the right sentence is not just one word we dont support that atm
                if len(right_tokens) != 1:
                    continue

                base_tokens = self.tokens[:reference_idx - 1]
                left_tokens = self.tokens[:reference_idx]

                self.tokens = left_tokens + [reference] + base_tokens + right_tokens

    def reverse_expression(self):
        """
        Function that inserts a not or removes it
        :return: The hypothesis reversed
        """
        # Cant reverse expression if not base expression
                if not self.is_base_expression:
            return

        # TODO decide if we want to use a flag for a expression or use not (currently)
        sentence_structure = detect_sentence_structure(self.tokens)

        if sentence_structure == 1 or sentence_structure == 2:
            self.tokens.insert(2, "not")
            return
        elif sentence_structure == 3 or sentence_structure == 4:
            if "not" in self.tokens:
                self.tokens.remove("not")
            elif "never" in self.tokens:
                self.tokens.remove("never")

            return

        raise ValueError(f'Hypothesis cant be reversed: {str(self)}')


    # the same method, but it uses exclamation mark instead
    def reverse_expression_mark(self):
        """
        Function that inserts a not or removes it
        :return: The hypothesis reversed
        """
        # Cant reverse expression if not base expression
        if not self.is_base_expression:
            return

        sentence_structure = detect_sentence_structure(self.tokens)

        if sentence_structure == 1 or sentence_structure == 2:
            self.tokens.insert(0, "!")
            return
        elif sentence_structure == 3 or sentence_structure == 4:
            if '!' in self.tokens:
                self.tokens.remove("!")
            else:
                self.tokens.remove("not")
            return

        raise ValueError(f'Hypothesis cant be reversed: {str(self)}')

    def is_tautologie_of(self, clause):

        if not self.is_base_expression or not clause.is_base_expression:
            return False

        shorter_clause = None
        longer_clause = None

        if len(self) == len(clause) + 1:
            shorter_clause = clause
            longer_clause = self
        elif len(self) == len(clause) - 1:
            shorter_clause = self
            longer_clause = clause
        else:
            return False

        # Go over each token check for equals and also if not is on the correct location
        # Probably not to smart :sweat_smile:
        j = 0
        for token in longer_clause.tokens:
            if token == "not" or token == "never" or token == "!" or token == "(" or token == ")":
                continue
            if token != shorter_clause.tokens[j]:
                return False
            j += 1

        return True

    def get_string_rep(self):
        return " ".join(self.tokens) if self.is_base_expression else self.init_hypo

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
