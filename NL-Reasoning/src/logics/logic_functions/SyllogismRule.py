from collections import defaultdict
from typing import List

from logics.Util import create_new_object
from logics.logic_functions.Rule import Rule
from logics.senteces.SyllogismExpression import SyllogismExpression


class SyllogismRule(Rule):

    def __init__(self, which_rule, expression, resulting_expression_1):
        self.name = 'Syllogism Rule'
        self.applicable = 'Syllogism Rule'
        if which_rule == 1:
            self.description = 'All x is A => attach object x to argument A for all cases'
        if which_rule == 2:
            self.description = 'Some x is A => introduce new object x for argument A'
        if which_rule == 3:
            self.description = 'None'
        if which_rule == 4:
            self.description = 'Reverse Conclusion for proof check'
        self.resulting_expression_1 = resulting_expression_1
        self.expression = expression

    def get_explanation(self, applied_rule):
        return dict(
            name=self.name,
            description=self.description,
            in_expression=[self.expression.get_string_rep()],
            out_expression=[
                [self.resulting_expression_1.get_string_rep()]
                if type(self.resulting_expression_1) != list else
                [expression.get_string_rep() for expression in self.resulting_expression_1]],
        )

    @staticmethod
    def apply_rule1(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'all':
            return new_clauses, None

        # Go over each class and search for a matching syllogism expression
        created_syllogism_expression = None
        for comp_clause in args[0]:
            if type(comp_clause) is not SyllogismExpression:
                continue
            if not comp_clause.is_individual:
                continue

            if clause.object != comp_clause.subject:
                continue

            created_syllogism_expression = SyllogismExpression(False, True, comp_clause.individual_keyword,
                                                               comp_clause.object,
                                                               clause.subject, )
            new_clauses[0] = [created_syllogism_expression]
            break
        return new_clauses, SyllogismRule(1, clause, created_syllogism_expression)

    @staticmethod
    def apply_rule2(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'some':
            return new_clauses, None

        first_individual_keyword = ['is', 'a']
        second_individual_keyword = ['is', 'a']
        if 'not' in clause.syllogism_keyword[1]:
            second_individual_keyword.insert(1, 'not')

        new_object = create_new_object("object", args[1])
        new_clauses[0] += [SyllogismExpression(
            False,
            True,
            first_individual_keyword,
            new_object,
            clause.object
        )]
        new_clauses[0] += [SyllogismExpression(
            False,
            True,
            second_individual_keyword,
            new_object,
            clause.subject
        )]
        return new_clauses, SyllogismRule(2, clause, new_clauses[0])

    @staticmethod
    def apply_rule3(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'no':
            return new_clauses, None

        # Go over each class and search for a matching syllogism expression
        for comp_clause in args[0]:
            if type(comp_clause) is not SyllogismExpression:
                continue
            if not comp_clause.is_individual:
                continue

            if clause.object != comp_clause.subject:
                continue

            individual_keyword = comp_clause.individual_keyword
            individual_keyword.insert(1, 'not')
            new_clauses[0] = [SyllogismExpression(
                False,
                True,
                individual_keyword,
                comp_clause.subject,
                clause.subject,
            )]
            break
        return new_clauses, SyllogismRule(3, clause, new_clauses[0]) if len(new_clauses) != 0 else None

    @staticmethod
    def apply_reverse(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses, None

        if not clause.negated:
            return new_clauses, None

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'all':
            new_clauses[0] += [SyllogismExpression(
                False,
                False,
                ("some", ['are', 'not']),
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'some':
            new_clauses[0] += [SyllogismExpression(
                False,
                False,
                ("no", ['is']),
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'no':
            new_clauses[0] += [SyllogismExpression(
                False,
                False,
                ("some", ['are']),
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keyword is None or clause.syllogism_keyword[0] == 'no':
            new_clauses[0] += [SyllogismExpression(
                False,
                False,
                ("all", ['are']),
                clause.object,
                clause.subject,
            )]
        return new_clauses, SyllogismRule(4, clause, new_clauses[0])
