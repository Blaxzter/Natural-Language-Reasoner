
class ParseException(Exception):

    def __init__(self, *args):

        if type(args[0]) == list:
            super(ParseException, self).__init__("In the parsing process was an error")
        else:
            super(ParseException, self).__init__(args)
