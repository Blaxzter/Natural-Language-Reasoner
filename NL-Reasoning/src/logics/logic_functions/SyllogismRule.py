from collections import defaultdict
from logics.logic_functions.Rule import Rule
from logics.LogicFunctions import create_new_object
from logics.senteces.SyllogismExpression import SyllogismExpression


class SyllogismRule(Rule):

    def __init__(self):
        self.name = 'Syllogism Rule'
        self.applicable = 'Syllogism Rule'

    def get_explanation(self, applied_rule):
        return f'html rule'

    def apply_rule1(self, clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'all':
            return new_clauses

        # Go over each class and search for a matching syllogism expression
        for comp_clause in args[0]:
            if type(comp_clause) is not SyllogismExpression:
                continue
            if not comp_clause.is_individual:
                continue

            if clause.object != comp_clause.subject:
                continue

            new_clauses[0] = [SyllogismExpression(
                False,
                True,
                comp_clause.individual_keyword,
                comp_clause.object,
                clause.subject,
            )]
            break
        return new_clauses

    def apply_rule2(self, clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'some':
            return new_clauses

        first_individual_keyword = ['is', 'a']
        second_individual_keyword = ['is', 'a']
        if 'not' in clause.syllogism_keyword[1]:
            second_individual_keyword.insert(1, 'not')

        new_clauses[0] += [SyllogismExpression(
            False,
            True,
            first_individual_keyword,
            create_new_object(clause.object, args[1]),
            clause.object
        )]
        new_clauses[0] += [SyllogismExpression(
            False,
            True,
            second_individual_keyword,
            create_new_object(clause.subject, args[1]),
            clause.subject
        )]
        return new_clauses

    def apply_rule3(self, clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses

        if clause.syllogism_keyword is None or clause.syllogism_keyword[0] != 'no':
            return new_clauses

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
        return new_clauses

    def apply_reverse(self, clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses

        if not clause.negated:
            return new_clauses

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
        return new_clauses