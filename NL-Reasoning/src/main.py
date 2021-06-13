from logics.senteces.Expression import Expression
from logics.TableauxSolver import TableauxSolver
from logics.senteces.Helper import create_expression

if __name__ == '__main__':

    # negation = 'Neither(john plays football and chess)'
    # negation = ['Neither', 'john', 'plays', 'football', 'and', 'chess']
    #
    # negation = ['((Neither (john plays football and chess)) or peter eats cheese)']
    # Expression(negation)

    hypo_1 = 'John plays football or chess'
    hypo_2 = 'If it is raining, John plays not football'
    hypo_3 = 'It is raining'
    #does not play football
    Expression.id_counter = 1

    test_exp_1 = create_expression(hypo_1)
    # test_exp_4 = Expression("Peter plays tennis and badminton")
    test_exp_2 = create_expression(hypo_2)
    test_exp_3 = create_expression(hypo_3)

    clause = create_expression("John never plays football")

    print(test_exp_1)
    print(test_exp_2)
    print(test_exp_3)
    # print(test_exp_4)
    print(clause)

    hypothesis = [test_exp_1, test_exp_2, test_exp_3]

    #%%

    solver = TableauxSolver(hypothesis, clause)
    result = solver.proof()

    for rule in solver.applied_rules:
        print(rule)

    #%%

    from graphviz import Source

    src = Source(solver.solve_tree.create_file())
    src.render('../solve-trees/first_example.gv', view=True)
