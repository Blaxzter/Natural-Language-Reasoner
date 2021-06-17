from typing import List

from logics.RuleCreatorUtil import create_root_node_rule, create_unification_rule, create_tautologie_rule
from logics.senteces.Expression import Expression
from logics.LogicFunctions import rule_set
from logics.senteces.BaseExpression import BaseExpression
from logics.senteces.FunctionExpression import FunctionExpression
from logics.senteces.UnifiableVariable import UnifiableVariable
from visualization.AppliedRule import AppliedRule
from visualization.TreeGenerator import TreeGenerator


class TableauxSolver:

    def __init__(self, hypothesis, thesis):
        self.hypothesis: List[Expression] = hypothesis
        self.thesis: Expression = thesis
        self.applied_rules = dict(root_node = create_root_node_rule())
        self.solve_tree = None
        self.all_branches_closed = True

    def proof(self):
        try:
            UnifiableVariable.used_variables = []
            clauses = []
            for claus in self.hypothesis:
                clauses.append(claus)
            neg_thesis = self.thesis.reverse_expression()
            clauses.append(neg_thesis)
            self.solve_tree = TreeGenerator(clauses)
            result = self.recursive_proof(
                clauses = clauses,
                applied_rules = [],
                list_of_new_objects = [],
                parent = self.solve_tree.root_node
            )
        except RuntimeError as e:
            print(e)
            raise e
        return result

    @staticmethod
    def check_for_tautology(hypothesis: BaseExpression, clauses: List[Expression], list_of_new_objects):
        for clause in clauses:
            if clause == hypothesis or not (type(clause) == BaseExpression or type(clause) == FunctionExpression):
                continue

            is_tautologie, unification_replacements = hypothesis.is_tautologie_of(clause, list_of_new_objects)
            if is_tautologie:
                return True, clause, unification_replacements
        return False, None, None

    def recursive_proof(self, clauses, applied_rules, list_of_new_objects, parent = None) -> bool:
        # Check if we have a tautology in this branch
        for i, curr_clause in enumerate(clauses):
            if not (type(curr_clause) == BaseExpression or type(curr_clause) == FunctionExpression):
                continue

            res, matched_clause, unification_replacements = TableauxSolver.check_for_tautology(curr_clause, clauses, list_of_new_objects)
            if res:
                node = parent
                if unification_replacements:
                    node = self.create_unification_replacements(curr_clause, matched_clause, unification_replacements, parent)

                # Found Tautology with the matched clause
                applied_rule = create_tautologie_rule(curr_clause, matched_clause)
                self.solve_tree.add_node(node, applied_rule, len(self.applied_rules))
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

                branches, created_rule = rule(curr_clause, clauses, list_of_new_objects)
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
                    return self.recursive_proof(
                        clauses = clauses,
                        applied_rules = applied_rules,
                        list_of_new_objects = list(list_of_new_objects),
                        parent = new_nodes[0]
                    )
                # If there is more then one branch we need to close every branch
                # Go over the list of clauses and create a recursive call for each
                closes = True
                for j, branch in branches.items():
                    next_clauses = list(clauses)
                    next_clauses += branch
                    branch_close = self.recursive_proof(
                        clauses = next_clauses,
                        applied_rules = list(applied_rules),
                        list_of_new_objects = list(list_of_new_objects),
                        parent = new_nodes[j]
                    )
                    if not branch_close:
                        closes = False

                # If not every branch closes then this doesnt work
                return closes

        # Tested every rule and didn't find anything applicable to close the branch
        self.all_branches_closed = False
        return False

    def create_unification_replacements(self, curr_clause, matched_clause, unification_replacements, parent):
        curr_parent = parent
        # Go over each unification and the both clauses and search for the unification variable,
        # Create the tree node and rule
        for unification in unification_replacements:
            for current_clause, comp_clause in [(curr_clause, matched_clause), (matched_clause, curr_clause)]:
                for var_idx, variable in enumerate(current_clause.variables):
                    if variable == unification[1]:
                        orig_sentence = current_clause.get_string_rep()
                        current_clause.variables[var_idx] = unification[0]
                        current_clause.tokenize_expression()
                        applied_rule = create_unification_rule(unification, current_clause, orig_sentence)
                        curr_parent = self.solve_tree.add_node(curr_parent, applied_rule, len(self.applied_rules))[0]
                        self.applied_rules[f"node_{len(self.applied_rules)}"] = applied_rule
        return curr_parent
