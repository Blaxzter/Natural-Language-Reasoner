"""
Small utils class that removes bulcks of code from the Tableaux solver
It just creates applied rules depending on what rule is required.
"""
from visualization.AppliedRule import AppliedRule

def create_root_node_rule():
    return AppliedRule(
            rule_name = "Root Node",
            referenced_line = 0,
            c_expression = None,
            rule_desc_obj = dict(
                name = "Reverse the premise",
                description = "In the root node we list all the given sentences. <br> "
                              "And have the sentence that is to be shown reversed.",
            )
        )

def create_tautologie_rule(curr_clause, matched_clause):
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
    return applied_rule


def create_unification_rule(unification, curr_clause, orig_sentence):
    applied_rule = AppliedRule(
        rule_name = "Unification Replacement",
        referenced_line = curr_clause.id,
        c_expression = curr_clause,
        created_expressions = {0: [curr_clause]},
        rule_desc_obj = dict(
            name = "Unification Replacement",
            description = "We have a quantified for all variable that needs to be replaced by a constant.",
            basic_in_expression = [str(unification[1])],
            basic_out_expression = [[unification[0]]],
            in_expression = [orig_sentence],
            out_expression = [[curr_clause.get_string_rep()]],
        )
    )
    return applied_rule