from collections import defaultdict

from logics.Constants import neg_function_keywords, separator, pos_middle_keywords, \
    neg_middle_keywords, get_opposite_of
from logics.logic_functions.Rule import Rule
from logics.senteces.FunctionExpression import FunctionExpression
from logics.senteces.SyllogismExpression import SyllogismExpression
from utils.Utils import create_new_object, list_in_check, list_eq_check


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
            name = self.name,
            description = self.description,
            in_expression = [self.expression.get_string_rep()]
            if type(self.expression) != list else
            [expression.get_string_rep() for expression in self.expression],
            out_expression = [
                [self.resulting_expression_1.get_string_rep()]
                if type(self.resulting_expression_1) != list else
                [expression.get_string_rep() for expression in self.resulting_expression_1]],
        )

    @staticmethod
    def apply_rule1(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if clause.negated or type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keywords is None or clause.syllogism_keywords[0] != 'all':
            return new_clauses, None

        # Go over each class and search for a matching syllogism expression
        created_syllogism_expression = None
        used_comp_clause = None
        for comp_clause in args[0]:
            if type(comp_clause) is not FunctionExpression:
                continue
            if comp_clause.multi:
                continue

            if clause.object != comp_clause.quantified_function:
                continue

            if list_in_check(neg_function_keywords, comp_clause.key_words):
                continue

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
        return new_clauses, SyllogismRule(1, [clause, used_comp_clause], created_syllogism_expression)

    @staticmethod
    def apply_rule2(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if clause.negated or type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keywords is None or clause.syllogism_keywords[0] != 'some':
            return new_clauses, None

        first_individual_keyword = ['is a']
        second_individual_keyword = ['is a']
        if 'not' in clause.syllogism_keywords[1]:
            second_individual_keyword = ['is not a']

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
        return new_clauses, SyllogismRule(2, clause, new_clauses[0])

    @staticmethod
    def apply_rule3(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if clause.negated or type(clause) is not SyllogismExpression:
            return new_clauses, None

        if clause.syllogism_keywords is None or clause.syllogism_keywords[0] != 'no':
            return new_clauses, None

        # Go over each class and search for a matching syllogism expression
        used_comp_clause = None
        for comp_clause in args[0]:
            if type(comp_clause) is not FunctionExpression:
                continue
            if comp_clause.multi:
                continue

            if clause.object != comp_clause.quantified_function:
                continue

            if list_in_check(neg_function_keywords, comp_clause.key_words):
                continue

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
        return new_clauses, SyllogismRule(3, [clause, used_comp_clause],
                                          new_clauses[0]) if used_comp_clause is not None else None

    @staticmethod
    def apply_reverse(clause: SyllogismExpression, *args):
        new_clauses = defaultdict(list)
        if type(clause) is not SyllogismExpression:
            return new_clauses, None

        if not clause.negated:
            return new_clauses, None

        pos_list_check = list_eq_check(pos_middle_keywords, clause.syllogism_keywords[1])
        neg_list_check = list_eq_check(neg_middle_keywords, clause.syllogism_keywords[1])
        if clause.syllogism_keywords[0] == 'all' and pos_list_check:
            new_clauses[0] += [SyllogismExpression(
                False,
                ["some", get_opposite_of(pos_list_check)],
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keywords[0] == 'some' and pos_list_check:
            middle_word = "has" if pos_list_check == "have" else "is"
            new_clauses[0] += [SyllogismExpression(
                False,
                ["no", middle_word],
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keywords[0] == 'no' and pos_list_check:
            new_clauses[0] += [SyllogismExpression(
                False,
                ["some", 'are'],
                clause.object,
                clause.subject,
            )]
        elif clause.syllogism_keywords[0] == 'some' and neg_list_check:
            new_clauses[0] += [SyllogismExpression(
                False,
                ["all", 'are'],
                clause.object,
                clause.subject,
            )]
        return new_clauses, SyllogismRule(4, clause, new_clauses[0])
