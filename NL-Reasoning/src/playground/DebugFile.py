#%%

from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Callable
from graphviz import Digraph

#%%


hypo_1 = 'John plays football or chess'
hypo_2 = 'When it is raining, John plays not football'
hypo_3 = 'It is raining'


#%%

def tokenize(sentence: str):
    tokens = sentence.split(" ")
    ret_tokens = []
    for i, token in enumerate(tokens):
        if ',' in token:
            c_token = token.split(',')
            ret_tokens.append(c_token[0])
            ret_tokens.append(',')
        else:
            ret_tokens.append(token)

    return ret_tokens


def detect_sentence_structure(sentence_tokens):
    if sentence_tokens is None or type(sentence_tokens) is not list or len(sentence_tokens) == 0:
        raise ValueError("Sentence structure detection only works for token lists. "
                         "And the token list is not empty")

    # TODO support multiple sentence base structures
    # does not play vs plays not ...
    # TODO maybe we need to do a bit more elaborate approach besides the length

    # Basic structure: A is B
    if len(sentence_tokens) == 3 and sentence_tokens[1] == "is":
        return 1

    # Basic structure: A does B
    if len(sentence_tokens) == 3:
        return 2

    # Inverted basic structure: A is not B
    if len(sentence_tokens) == 4 and sentence_tokens[1] == "is":
        return 3

    # Inverted basic structure: A does not B
    # Split because maybe we want to check: A does not do B or doesn't
    if len(sentence_tokens) == 4:
        return 4

    raise ValueError(f'Sentence structure is not detected: {str(sentence_tokens)}')


#%%

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

        # A base expression has a few cases
        self.is_base_expression = False
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
            if token == "not":
                continue
            if token != shorter_clause.tokens[j]:
                return False
            j += 1

        return True

    def get_string_rep(self):
        return " ".join(self.tokens)

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

        return param in self.tokens

    def get_applicable_token(self, split_token):
        # Simple structure expected for now explanation further down for now just a in check
        # TODO more elaborate // Add hierarchical structure
        if split_token == 'and' or split_token == 'or':
            return self.tokens.index(split_token)
        elif split_token == 'when':
            # Probably dont want to support hierarchical structures with when expression
            return self.tokens.index(',')

        raise NotImplementedError("The rule has not been implemented yet.")


#%%

exp = Expression(hypo_3)
print(exp)
exp.reverse_expression()
print(exp)
exp.reverse_expression()
print(exp)

#%%

exp_1 = Expression(hypo_3)
exp_2 = Expression(hypo_3)
exp_2.reverse_expression()

print(exp_1.is_tautologie_of(exp_2))
print(exp_2.is_tautologie_of(exp_1))
print(exp_2.is_tautologie_of(exp_2))
print(exp_1.is_tautologie_of(exp_1))


#%%

# Assume simple structure for now with a and b ... no a and b or c and d
# For that we would need to do a binding check or something and convert
# the Expression into a hierarchical structure and call something like is applicable
# In the case of a and b or c and d it would be like this (a and b) or (c and d) and i
# dont think you can apply the and rule here

def simple_split_rule(clause: Expression, split_token: str):
    # if the rule is not applicable then return empty list
    if not clause.is_applicable(split_token):
        return []

    index_of_rule = clause.get_applicable_token(split_token)
    return [Expression(clause.tokens[:index_of_rule]), Expression(clause.tokens[index_of_rule + 1:])]


def and_rule(clause: Expression) -> Dict:
    new_clauses = defaultdict(list)

    split_token = 'and'
    split_expressions = simple_split_rule(clause, split_token)
    if len(split_expressions) != 0:
        new_clauses[0] += split_expressions
    return new_clauses


def or_rule(clause: Expression) -> Dict:
    new_clauses = defaultdict(list)

    split_token = 'or'
    split_expressions = simple_split_rule(clause, split_token)
    for i, split_expression in enumerate(split_expressions):
        new_clauses[i].append(split_expression)
    return new_clauses


def when_rule(clause: Expression):
    new_clauses = defaultdict(list)

    if not clause.is_applicable('when'):
        return new_clauses

    split_index = clause.get_applicable_token('when')
    left_tokens = list(clause.tokens[:split_index])
    right_tokens = list(clause.tokens[split_index + 1:])

    if 'when' in left_tokens:
        when_token = left_tokens
        not_when_token = right_tokens
    else:
        not_when_token = left_tokens
        when_token = right_tokens

    when_token.remove('when')
    when_expression = Expression(when_token)
    when_expression.reverse_expression()
    new_clauses[0].append(when_expression)
    new_clauses[1].append(Expression(not_when_token))
    return new_clauses


# Order is important, try to not branch to early
rule_set: Dict[str, Callable[[Expression], Dict[int, Expression]]] = dict(
    and_rule = and_rule,
    or_rule = or_rule,
    when_rule = when_rule,
)


#%%

@dataclass()
class AppliedRule:
    rule_name: str = field()
    referenced_line: int = field()
    c_expression: Expression = field(default = None, compare = False, hash = False)
    matched_expression: Expression = field(default = None, compare = False, hash = False)
    created_expressions: List[Expression] = field(default = None, compare = False, hash = False)

    def __lt__(self, other):
        return len(self.position) - len(other.position)

#%%

import pydot


class TreeGenerator:

    def __init__(self, premise):
        self.graph = pydot.Dot('applied_rules', graph_type = 'graph')
        self.root_node = pydot.Node(0, label = self.get_rule_string(premise, "Initial root", None), shape = 'none')
        self.graph.add_node(self.root_node)
        self.node_id = 1

    def add_node(self, parent_node, applied_rule):
        new_nodes = []

        if applied_rule.created_expressions is None:
            new_node = pydot.Node(self.node_id, label = f'{self.get_rule_string([applied_rule.c_expression, applied_rule.matched_expression], applied_rule.rule_name, applied_rule.referenced_line)}', shape = 'none')
            self.graph.add_node(new_node)
            my_edge = pydot.Edge(parent_node.get_name(), str(self.node_id))
            self.graph.add_edge(my_edge)
            self.node_id += 1
            new_nodes.append(new_node)
        else:
            for new_exp in applied_rule.created_expressions.values():
                new_node = pydot.Node(self.node_id, label = f'{self.get_rule_string(new_exp, applied_rule.rule_name, applied_rule.referenced_line)}', shape = 'none')
                self.graph.add_node(new_node)

                my_edge = pydot.Edge(parent_node.get_name(), str(self.node_id))
                self.graph.add_edge(my_edge)
                self.node_id += 1
                new_nodes.append(new_node)
        return new_nodes

    def get_rule_string(self, expression, rule_name, reference_line):

        sorted_exp = sorted(expression, key = lambda expr: expr.id)

        reference_line_str = f'<td ROWSPAN="{len(expression)}" SIDES="L">{reference_line}</td>' if reference_line is not None or rule_name == 'tautologie' else ""

        tautologie_line = ""
        table_head = f'<tr><td COLSPAN="3" ALIGN="CENTER" SIDES="B">{rule_name}</td></tr>'
        if rule_name == 'tautologie':
            tautologie_line = f'<tr><td COLSPAN="3" ALIGN="CENTER" SIDES="T">X</td></tr>'
            table_head = ''

        return f'''<
        <table border="0" CELLBORDER="1">
        {table_head}
        {''.join([f'<tr><td BORDER="0" CELLSPACING="10">{orig.id}:</td><td BORDER="0" ALIGN="LEFT">{orig.get_string_rep()}</td>{reference_line_str if i == 0 else ""}</tr>' for i, orig in enumerate(sorted_exp)])}
        {tautologie_line}
        </table>
        >'''
        # return '\n'.join([' '.join(item.tokens) for item in expression])

    def create_file(self):
        return self.graph.to_string()

#%%

class TableauxSolver:

    def __init__(self, hypothesis, thesis):

        self.hypothesis: List[Expression] = hypothesis
        self.thesis: Expression = thesis
        self.applied_rules = []
        self.solve_tree = None

    def proof(self):
        try:
            clauses = []
            for claus in self.hypothesis:
                clauses.append(claus)
            self.thesis.reverse_expression()
            clauses.append(self.thesis)
            self.solve_tree = TreeGenerator(clauses)
            result = self.recursive_proof(clauses, [], parent = self.solve_tree.root_node)
        except RuntimeError as e:
            print(e)
            raise e
        return result

    @staticmethod
    def check_for_tautology(hypothesis: Expression, clauses: List[Expression]):
        for clause in clauses:
            if clause == hypothesis:
                continue
            if hypothesis.is_tautologie_of(clause):
                return True, clause
        return False, None

    def recursive_proof(self, clauses, applied_rules, parent = None) -> bool:
        # Check if we have a tautology in this branch
        for i, curr_clause in enumerate(clauses):

            res, matched_clause = TableauxSolver.check_for_tautology(curr_clause, clauses)
            if res:
                # Found Tautology with the matched clause
                applied_rule = AppliedRule(
                    rule_name = "tautologie",
                    referenced_line = curr_clause.id,
                    c_expression = curr_clause,
                    matched_expression = matched_clause,
                )
                self.applied_rules.append(applied_rule)
                self.solve_tree.add_node(parent, applied_rule)
                return True

        # Go over each clause and check if we can apply a rule
        # Keep the branching clauses to the end
        for rule_name, rule in rule_set.items():
            for i, curr_clause in enumerate(clauses):

                # Dont apply rule twice
                applied_rule = AppliedRule(
                    rule_name = rule_name,
                    referenced_line = curr_clause.id,
                    c_expression = curr_clause
                )
                if applied_rule in applied_rules:
                    continue

                branches = rule(curr_clause)
                new_nodes = None

                if len(branches) != 0:
                    applied_rule.created_expressions = branches
                    applied_rules.append(applied_rule)
                    self.applied_rules.append(applied_rule)
                    new_nodes = self.solve_tree.add_node(parent, applied_rule)
                else:
                    continue

                # if only one branch then we just add the rules to the current set and return
                # the recursive call
                if len(branches) == 1:
                    clauses += branches[0]  # Not sure if we want to create a copy of the list
                    return self.recursive_proof(clauses, applied_rules, new_nodes[0])

                # If there is more then one branch we need to close every branch
                # Go over the list of clauses and create a recursive call for each
                closes = True
                for j, branch in branches.items():
                    next_clauses = list(clauses)
                    next_clauses += branch
                    branch_close = self.recursive_proof(next_clauses, list(applied_rules), new_nodes[j])
                    if not branch_close:
                        closes = False

                # If not every branch closes then this doesnt work
                return closes

        # Tested every rule and didn't find anything applicable to close the branch
        return False


#%%

Expression.id_counter = 1

test_exp_1 = Expression(hypo_1)
test_exp_4 = Expression("Peter plays tennis and badminton")
test_exp_2 = Expression(hypo_2)
test_exp_3 = Expression(hypo_3)

clause = Expression("John plays not football")

print(test_exp_1)
print(test_exp_2)
print(test_exp_3)
print(test_exp_4)
print(clause)

hypothesis = [test_exp_1, test_exp_2, test_exp_3, test_exp_4]

#%%

solver = TableauxSolver(hypothesis, clause)
result = solver.proof()

for rule in solver.applied_rules:
    print(rule)

#%%

from graphviz import Source

src = Source(solver.solve_tree.create_file())
src.render('solve-trees/first_example.gv', view=True)