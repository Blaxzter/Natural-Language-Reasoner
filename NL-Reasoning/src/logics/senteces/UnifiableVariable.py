
class UnifiableVariable:
    """
    Class that represents a unifiable variable
    """

    used_variables = []

    def __init__(self, original_variable):
        """
        Creates the unifiable variable based on the original variable
        :param original_variable: The to be replaced original variable
        """
        # Create a new name for the to be replaced variable
        replace_variable = original_variable
        if original_variable in UnifiableVariable.used_variables:
            count = 0
            for used_variable in UnifiableVariable.used_variables:
                if original_variable in used_variable:
                    count += 1
            replace_variable = f'{replace_variable}_{count}'

        # Add the name of the to be replaced variable to the list
        UnifiableVariable.used_variables.append(replace_variable)
        self.original_variable = replace_variable

    def __str__(self):
        """
        Return the string rep of this unifiable variable
        :return:
        """
        return f'any {self.original_variable}'
