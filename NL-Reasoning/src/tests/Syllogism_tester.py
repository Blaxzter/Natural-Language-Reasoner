"""
File that loads all the examples in the syllogism data set and returns
"""
import json
import pandas as pd

from logics.senteces.Helper import create_expression
from logics.senteces.SyllogismExpression import SyllogismExpression
from src.logics.NaturalTableauxSolver import NaturalTableauxSolver

if __name__ == '__main__':

    f = open('../data/syllogism-data.json', )
    data = json.load(f)
    df = pd.DataFrame(data)
    result = []
    for i in range(0, len(data)):
        expressions = [data[i]["premise_1"],
                       data[i]["premise_2"]]
        to_be_shown = data[i]["conclusion"]
        nts = NaturalTableauxSolver(expressions, to_be_shown)

        for parsed_expression, original_expression in zip(nts.expressions + [nts.to_be_shown], [data[i]["premise_1"], data[i]["premise_2"], data[i]["conclusion"]]):
            if type(parsed_expression) != SyllogismExpression:
                create_expression(original_expression)
                print(f'Wrong expression parsed: {parsed_expression}')

        nts.solve()
        ans = nts.tableaux_is_closed()

        is_valid = 'invalid' in data[i]["valid"]
        if ans == is_valid:
            print(ans, data[i]["valid"], expressions, to_be_shown)
        result.append(ans)

    # df['result'] = result
    # df.to_csv('output_final.csv', index=False)


