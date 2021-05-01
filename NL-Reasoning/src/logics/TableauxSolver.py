from typing import List

from logics.Expression import Expression
from logics.LogicFunctions import rule_set
from visualization.AppliedRule import AppliedRule
from visualization.TreeGenerator import TreeGenerator


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