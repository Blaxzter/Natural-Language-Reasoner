import json
import pandas as pd

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
        nts.solve()
        ans = nts.tableaux_is_closed()
        result.append(ans)

    df['result'] = result
    df.to_csv('output_final.csv', index=False)


