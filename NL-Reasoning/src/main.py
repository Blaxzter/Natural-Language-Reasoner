from src.logics.Expression import Expression
from src.logics.TableauxSolver import TableauxSolver

if __name__ == '__main__':

    hypo_1 = 'John plays football or chess'
    hypo_2 = 'When it is raining, John plays not football'
    hypo_3 = 'It is raining'

    Expression.id_counter = 1

    test_exp_1 = Expression(hypo_1)
    test_exp_4 = Expression("Peter plays tennis and badminton")
    test_exp_2 = Expression(hypo_2)
    test_exp_3 = Expression(hypo_3)

    clause = Expression("John plays not football")

    print(test_exp_1)
    print(test_exp_2)
    print(test_exp_3)
    print(test_exp_4)
    print(clause)

    hypothesis = [test_exp_1, test_exp_2, test_exp_3, test_exp_4]

    #%%

    solver = TableauxSolver(hypothesis, clause)
    result = solver.proof()

    for rule in solver.applied_rules:
        print(rule)

    #%%

    from graphviz import Source

    src = Source(solver.solve_tree.create_file())
    src.render('../solve-trees/first_example.gv', view=True)
