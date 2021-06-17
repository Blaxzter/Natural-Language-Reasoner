
class UnifiableVariable:

    used_variables = []

    def __init__(self, original_variable):

        replace_variable = original_variable
        if original_variable in UnifiableVariable.used_variables:
            count = 0
            for used_variable in UnifiableVariable.used_variables:
                if original_variable in used_variable:
                    count += 1
            replace_variable = f'{replace_variable}_{count}'

        UnifiableVariable.used_variables.append(replace_variable)
        self.original_variable = replace_variable

    def __str__(self):
        return f'any {self.original_variable}'
