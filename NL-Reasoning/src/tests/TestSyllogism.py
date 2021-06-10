from logics.NaturalTableauxSolver import NaturalTableauxSolver
from graphviz import Source

if __name__ == '__main__':
    expressions = [
        "All humans are mortal",
        "All Greeks are human",
    ]
    to_be_shown = "Therefore, all greeks are mortal"

    nts = NaturalTableauxSolver(expressions, to_be_shown)

    nts.solve()

    src = Source(nts.get_dot_graph())
    src.render('../solve-trees/syllogism.gv', view=True)
