"""
Here i tested different sentences that should work
"""
from logics.senteces.Helper import create_expression

if __name__ == '__main__':
    # Create test sentences
    sentences = [
        "When i love you then you love me",
        "all persons are mortal",
        "x is a parent of y",
        "it is raining",
        "if x is a parent of y, then x is older than y",
    ]

    for sentence in sentences:
        expression = create_expression(sentence)
        print(expression)
