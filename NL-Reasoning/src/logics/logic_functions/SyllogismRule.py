from collections import defaultdict

from logics.Constants import neg_function_keywords, separator, pos_middle_keywords, \
    neg_middle_keywords, get_opposite_of
from logics.logic_functions.Rule import Rule
from logics.senteces.FunctionExpression import FunctionExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from utils.Utils import create_new_object, list_in_check, list_eq_check


class SyllogismRule(Rule):
    """
    Class representing the application of all Syllogism rules
    It is required for the tool tip
    """

    def __init__(self, which_rule, expression, resulting_expression, neg_case = -1):
        self.name = 'Syllogism Rule'
        self.applicable = 'Syllogism Rule'
        self.which_rule = which_rule
        self.neg_case = neg_case
        if which_rule == 1:
            self.description = 'All x is A => attach object x to argument A for all cases'
        if which_rule == 2:
            self.description = 'Some x is (not) A => introduce new object x for argument A'
        if which_rule == 3:
            self.description = 'No x is A => attach object x to argument A for all cases'
        if which_rule == 4:
            self.description = 'Reverse Conclusion for proof check.'
        self.resulting_expression = resulting_expression
        self.expression = expression

    def get_explanation(self):
        """
        :return: Create the explanation based on the provided data in the object.
        """

        # Create all the basic rule expressions for
        basic_in_expression = ["all X are Y", "N is a(n) X"],
        basic_out_expression = [["N is a(n) Y"]],
        if self.which_rule == 2:
            basic_in_expression = ["some X are (not) Y"],
            basic_out_expression = [["O is a(n) X", "O is a(n) Y"]],
        if self.which_rule == 3:
            basic_in_expression = ["no X is Y", "N is a(n) X"],
            basic_out_expression = [["N is not a(n) Y"]],
        if self.which_rule == 4:
            if self.neg_case == 1:
                basic_in_expression = ["it is not the case that all X are Y"],
                basic_out_expression = [["some X are not Y"]],
            if self.neg_case == 2:
                basic_in_expression = ["it is not the case that some X are Y"],
                basic_out_expression = [["no X is Y"]],
            if self.neg_case == 3:
                basic_in_expression = ["it is not the case that no X is Y"],
                basic_out_expression = [["some X are Y"]],
            if self.neg_case == 4:
                basic_in_expression = ["it is not the case that some X are not Y"],
                basic_out_expression = [["all X are Y"]],

        # Create the rule explanation for the tooltip
        return dict(
            name = self.name,
            description = self.description,
            basic_in_expression = basic_in_expression,
            basic_out_expression = basic_out_expression,
            in_expression = [self.expression.get_string_rep()]
            if type(self.expression) != list else
            [expression.get_string_rep() for expression in self.expression],
            out_expression = [
                [self.resulting_expression.get_string_rep()]
                if type(self.resulting_expression) != list else
                [expression.get_string_rep() for expression in self.resulting_expression]],
        )

    @staticmethod
    def apply_rule1(clause: SyllogismExpression, *args):
        """
        Apply the first syllogism rule which when applicable: all X are Y", "N is a(n) X
        Attaches the N to the Object Y ->  N is a(n) Y
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """

        # Check for applicable and for the correct keyword
        new_clauses = defaultdict(list)
        if clause.negated or type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keywords is None or clause.syllogism_keywords[0] != 'all':
            return new_clauses, None

        # Go over each class and search for a matching syllogism expression
        created_syllogism_expression = None
        used_comp_clause = None
        for comp_clause in args[0]:
            # Do all the application checks
            if type(comp_clause) is not FunctionExpression:
                continue

            if comp_clause.multi:
                continue

            if clause.object != comp_clause.quantified_function:
                continue

            if list_in_check(neg_function_keywords, comp_clause.key_words):
                continue

            # If found create the respective clause
            used_comp_clause = comp_clause
            created_syllogism_expression = FunctionExpression(
                False,
                comp_clause.variables,
                clause.subject,
                comp_clause.key_words,
                False
            )
            new_clauses[0] = [created_syllogism_expression]
            break
        # Return the branches and create the rule description
        return new_clauses, SyllogismRule(1, [clause, used_comp_clause], created_syllogism_expression)

    @staticmethod
    def apply_rule2(clause: SyllogismExpression, *args):
        """
        Apply the second syllogism rule which when applicable: some X are (not) Y
        Creates O is a(n) X, O is a(n) Y
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """

        # Check for applicable and for the correct keyword
        new_clauses = defaultdict(list)
        if clause.negated or type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keywords is None or clause.syllogism_keywords[0] != 'some':
            return new_clauses, None

        # As this rule is for both some rules we insert a not
        first_individual_keyword = ['is a']
        second_individual_keyword = ['is a']
        if 'not' in clause.syllogism_keywords[1]:
            second_individual_keyword = ['is not a']

        # Create the function expressions
        new_object = create_new_object(args[1])
        new_clauses[0] += [FunctionExpression(
            False,
            [new_object],
            clause.object,
            first_individual_keyword,
            False
        )]
        new_clauses[0] += [FunctionExpression(
            'not' in clause.syllogism_keywords[1],
            [new_object],
            clause.subject,
            second_individual_keyword,
            False
        )]
        # Return the branches and create the rule description
        return new_clauses, SyllogismRule(2, clause, new_clauses[0])

    @staticmethod
    def apply_rule3(clause: SyllogismExpression, *args):
        """
        Apply the third syllogism rule which when applicable: no X is Y, N is a(n) X
        Attaches the N to the Object Y ->  N is not a(n) Y
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """

        # Check for applicable and for the correct keyword
        new_clauses = defaultdict(list)
        if clause.negated or type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keywords is None or clause.syllogism_keywords[0] != 'no':
            return new_clauses, None

        # Go over each class and search for a matching syllogism expression
        used_comp_clause = None
        for comp_clause in args[0]:
            # Do all the application checks
            if type(comp_clause) is not FunctionExpression:
                continue
            if comp_clause.multi:
                continue

            if clause.object != comp_clause.quantified_function:
                continue

            if list_in_check(neg_function_keywords, comp_clause.key_words):
                continue

            # If found create the respective clause
            used_comp_clause = comp_clause
            new_keyword = comp_clause.key_words[0].split(separator)
            new_keyword.insert(1, 'not')

            new_clauses[0] = [FunctionExpression(
                True,
                comp_clause.variables,
                clause.subject,
                [separator.join(new_keyword)],
                False
            )]
            break
        # Return the branches and create the rule description
        return new_clauses, SyllogismRule(3, [clause, used_comp_clause],
                                          new_clauses[0]) if used_comp_clause is not None else None

    @staticmethod
    def apply_reverse(clause: SyllogismExpression, *args):
        """
        Reverse the respective expression
        :param clause: The clause to which the rule is applied to
        :param args: The remaining args being the other clauses, list_of_new_objects
        :return: Dictionary containing the branches. Each branch containing a list of created expressions.
        """

        # Check for applicable and for the correct keyword
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses, None

        if not clause.negated:
            return new_clauses, None

        # Get what positive or negative keyword was used
        pos_list_check = list_eq_check(pos_middle_keywords, clause.syllogism_keywords[1])
        neg_list_check = list_eq_check(neg_middle_keywords, clause.syllogism_keywords[1])
        # Check each syllogism case
        neg_case = 0
        if clause.syllogism_keywords[0] == 'all' and pos_list_check:
            neg_case = 1
            new_clauses[0] += [SyllogismExpression(
                False,
                ["some", get_opposite_of(pos_list_check)],
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keywords[0] == 'some' and pos_list_check:
            neg_case = 2
            middle_word = "has" if pos_list_check == "have" else "is"
            new_clauses[0] += [SyllogismExpression(
                False,
                ["no", middle_word],
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keywords[0] == 'no' and pos_list_check:
            neg_case = 3
            new_clauses[0] += [SyllogismExpression(
                False,
                ["some", 'are'],
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keywords[0] == 'some' and neg_list_check:
            neg_case = 4
            new_clauses[0] += [SyllogismExpression(
                False,
                ["all", 'are'],
                clause.object,
                clause.subject,
            )]
        # Return the branches and create the rule description
        return new_clauses, SyllogismRule(4, clause, new_clauses[0], neg_case)
