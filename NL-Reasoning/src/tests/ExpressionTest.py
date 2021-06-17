from logics.NaturalTableauxSolver import NaturalTableauxSolver
from logics.senteces.Helper import create_expression

if __name__ == '__main__':
    sentence = "When i love you then you love me"
    sentence = "all persons are mortal"
    sentence = "x is a parent of y"
    sentence = "it is raining"
    sentence = "if x is a parent of y, then x is oder then y"
    expression = create_expression(sentence)
    print(expression)
