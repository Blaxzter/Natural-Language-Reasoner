from typing import List

from logics.senteces.Expression import Expression
from logics.LogicFunctions import rule_set
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from visualization.AppliedRule import AppliedRule
from visualization.TreeGenerator import TreeGenerator


class TableauxSolver:

    def __init__(self, hypothesis, thesis):
        self.hypothesis: List[Expression] = hypothesis
        self.thesis: Expression = thesis
        self.applied_rules = {
            'root_node': AppliedRule(
                rule_name = "Root Node",
                referenced_line = 0,
                c_expression = None,
                rule_desc_obj = dict(
                    name = "Reverse the premise",
                    description = "In the root node we list all the given sentences. <br> "
                                  "And have the sentence that is to be shown reversed.",
                )
            )
        }
        self.list_of_new_objects = []
        self.solve_tree = None
        self.all_branches_closed = True

    def proof(self):
        try:
            clauses = []
            for claus in self.hypothesis:
                clauses.append(claus)
            neg_thesis = self.thesis.reverse_expression()
            clauses.append(neg_thesis)
            self.solve_tree = TreeGenerator(clauses)
            result = self.recursive_proof(clauses, [], parent = self.solve_tree.root_node)
        except RuntimeError as e:
            print(e)
            raise e
        return result

    @staticmethod
    def check_for_tautology(hypothesis: BaseExpression, clauses: List[Expression]):
        for clause in clauses:
            if clause == hypothesis or not (type(clause) == BaseExpression or type(clause) == SyllogismExpression):
                continue

            if hypothesis.is_tautologie_of(clause):
                return True, clause
        return False, None

    def recursive_proof(self, clauses, applied_rules, parent = None) -> bool:
        # Check if we have a tautology in this branch
        for i, curr_clause in enumerate(clauses):
            if not (type(curr_clause) == BaseExpression or type(curr_clause) == SyllogismExpression):
                continue

            res, matched_clause = TableauxSolver.check_for_tautology(curr_clause, clauses)
            if res:
                # Found Tautology with the matched clause
                applied_rule = AppliedRule(
                    rule_name = "Tautologie",
                    referenced_line = curr_clause.id,
                    c_expression = curr_clause,
                    matched_expression = matched_clause,
                    rule_desc_obj = dict(
                        name = "Tautologie",
                        description = "This means we have found an expression that shows the opposite.",
                        basic_in_expression = ["¬A ∧ A"],
                        basic_out_expression = ["X"],
                        in_expression = [curr_clause.get_string_rep(), matched_clause.get_string_rep()],
                        out_expression = [["X"]],
                    )
                )
                self.solve_tree.add_node(parent, applied_rule, len(self.applied_rules))
                self.applied_rules[f"node_{len(self.applied_rules)}"] = applied_rule
                return True

        # Go over each clause and check if we can apply a rule
        # Keep the branching clauses to the end
        for rule_name, rule in rule_set.items():
            for i, curr_clause in enumerate(clauses):

                # Dont apply rule twice
                applied_rule = AppliedRule(
                    rule_name = rule_name,
                    referenced_line = curr_clause.id,
                    c_expression = curr_clause,
                )
                if applied_rule in applied_rules:
                    continue

                branches, created_rule = rule(curr_clause, clauses, self.list_of_new_objects)
                new_nodes = None

                if len(branches) != 0:
                    applied_rule.created_expressions = branches
                    rule_explanation = created_rule.get_explanation(applied_rule)
                    applied_rule.rule_desc_obj = rule_explanation
                    applied_rules.append(applied_rule)
                    new_nodes = self.solve_tree.add_node(parent, applied_rule, len(self.applied_rules))
                    self.applied_rules[f"node_{len(self.applied_rules)}"] = applied_rule
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
        self.all_branches_closed = False
        return False
