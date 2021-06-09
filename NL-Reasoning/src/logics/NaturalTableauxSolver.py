from logics.Expression import Expression
from logics.TableauxSolver import TableauxSolver
from logics.senteces.Helper import create_expression


class NaturalTableauxSolver:

    def __init__(self, clauses, to_be_shown):
        Expression.id_counter = 0
        self.expressions = [
            create_expression(clause) for clause in clauses
        ]
        self.to_be_shown = create_expression(to_be_shown)

        self.solver = TableauxSolver(self.expressions, self.to_be_shown)

    def solve(self):
        return self.solver.proof()

    def get_applied_rules(self):
        return self.solver.applied_rules

    def get_dot_graph(self):
        return self.solver.solve_tree.create_file()
