from src.logics.Expression import Expression
from src.logics.TableauxSolver import TableauxSolver


class NaturalTableauxSolver:

    def __init__(self, clauses, to_be_shown):
        self.expressions = [
            Expression(clause) for clause in clauses
        ]
        self.to_be_shown = Expression(to_be_shown)

        self.solver = TableauxSolver(self.expressions, self.to_be_shown)

    def solve(self):
        return self.solver.proof()

    def get_applied_rules(self):
        return self.solver.applied_rules

    def get_dot_graph(self):
        return self.solver.solve_tree.create_file()
