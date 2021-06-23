from logics.senteces.Expression import Expression
from logics.TableauxSolver import TableauxSolver
from logics.senteces.Helper import create_expression


class NaturalTableauxSolver:
    """
    Wrapper class for the tableaux solver that parses the
    expressions and calls the solver
    """

    def __init__(self, clauses, to_be_shown):
        Expression.id_counter = 0
        self.expressions = [
            create_expression(clause) for clause in clauses if len(clause) != 0
        ]
        self.to_be_shown = create_expression(to_be_shown)

        self.solver = TableauxSolver(self.expressions, self.to_be_shown)

    def solve(self):
        return self.solver.proof()

    def get_applied_rules(self):
        return self.solver.applied_rules

    def tableaux_is_closed(self):
        return self.solver.all_branches_closed

    def get_dot_graph(self):
        return self.solver.solve_tree.create_file()
