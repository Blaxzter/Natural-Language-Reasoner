
class ParseException(Exception):
    """
    New exception for the sentence parsing
    """
    def __init__(self, *args):

        if type(args[0]) == list:
            super(ParseException, self).__init__("In the parsing process was an error")
            self.exception_list = args[0]
        else:
            super(ParseException, self).__init__(args)
            self.exception_list = [args[0]]
