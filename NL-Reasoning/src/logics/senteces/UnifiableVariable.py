
class UnifiableVariable:
    def __init__(self, original_variable):
        self.original_variable = original_variable

    def __str__(self):
        return f'any {self.original_variable}'