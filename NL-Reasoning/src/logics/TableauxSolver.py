"""
File containing the majority of the tableaux logic
"""

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
    """
    Class that contains the logic for the tableaux method
    """

    def __init__(self, hypothesis, thesis):
        self.hypothesis: List[Expression] = hypothesis
        self.to_be_shown: Expression = thesis
        self.applied_rules = dict(root_node = create_root_node_rule())
        self.solve_tree = None
        self.all_branches_closed = True

    def proof(self):
        """
        The tableaux solver entry point that reverses the to be shown expression
        and calls the recursive solver with the initial parameters.

        It also creates the tree generator for the tableaux method
        :return: Whether the conclusion holds or not
        """
        try:
            # Set the unifiable variables to new
            UnifiableVariable.used_variables = []
            # Create a clean clauses list
            clauses = []
            for claus in self.hypothesis:
                clauses.append(claus)
            # Reverse the expression and append it to the clause list
            neg_thesis = self.to_be_shown.reverse_expression()
            clauses.append(neg_thesis)

            # Create the solve tree and call the recursive proof
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
        """
        Helper function that checks for the given hypothesis if there is a tautology in the created classes
        :param hypothesis:          The expression to check with
        :param clauses:             The list of clauses
        :param list_of_new_objects: If we need to creat a new object in the process
        :return: If branch is closed, the clause it was closed with, the used unification replacements
        """
        # Go over each clause and check whether it is a base or a function expression
        for clause in clauses:
            if clause == hypothesis or not (type(clause) == BaseExpression or type(clause) == FunctionExpression):
                continue

            # If it is check if it is a tautologie with the hypothesis expression
            is_tautologie, unification_replacements = hypothesis.is_tautologie_of(clause, list_of_new_objects)
            if is_tautologie:
                return True, clause, unification_replacements
        return False, None, None

    def recursive_proof(self, clauses, applied_rules, list_of_new_objects, parent = None) -> bool:
        """
        The recursive prove first searches for a tautology.
        If none is found try to apply a rule.
        If one is applied successfully call the recursive proof with the new clause.
        Otherwise return false

        :param clauses:             The list of clauses in current branch
        :param applied_rules:       The all ready applied rules in this branch
        :param list_of_new_objects: The list of new objects that were created in this branch
        :param parent:              The tree node parent for this branch
        :return: If the branch closes or not
        """

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

                # Apply rule and check if we have created branches
                branches, created_rule = rule(curr_clause, clauses, list_of_new_objects)
                new_nodes = None

                # If we have add the node to the documentation otherwise continue
                if len(branches) != 0:
                    applied_rule.created_expressions = branches
                    rule_explanation = created_rule.get_explanation()
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
        """
        This function creates unification replacements for the visualization
        :param curr_clause:                 The clause that was found for the tautology
        :param matched_clause:              The matched tautology
        :param unification_replacements:    The used unification replacements
        :param parent:                      The tree node
        :return: The last parent that was used
        """
        curr_parent = parent
        # Go over each unification and the both clauses and search for the unification variable,
        # Create the tree node and rule
        for unification in unification_replacements:
            # Go over the order of the matched pair
            for current_clause, comp_clause in [(curr_clause, matched_clause), (matched_clause, curr_clause)]:
                # If its a function expression get the variable list otherwise geht the object and subject
                var_list = current_clause.variables if type(curr_clause) == FunctionExpression else [current_clause.object, current_clause.subject]
                # Iterate over the variables
                for var_idx, variable in enumerate(var_list):
                    # Search for the unified variable and replace it
                    if variable == unification[1]:
                        # Get the original sentence for displaying
                        orig_sentence = current_clause.get_string_rep()
                        # Replace it
                        if type(curr_clause) == BaseExpression:
                            if var_idx == 0:
                                current_clause.object = unification[0]
                            else:
                                current_clause.subject = unification[0]
                        else:
                            current_clause.variables[var_idx] = unification[0]

                        # Re Tokenize and create the rule
                        current_clause.tokenize_expression()
                        applied_rule = create_unification_rule(unification, current_clause, orig_sentence)
                        curr_parent = self.solve_tree.add_node(curr_parent, applied_rule, len(self.applied_rules))[0]
                        self.applied_rules[f"node_{len(self.applied_rules)}"] = applied_rule
        return curr_parent
