
separator = ' '
negation_keywords = ['not', 'never']
connection_keywords = ['or', 'and', ';']
when_keywords = ['when', 'if']
when_split_tokens = [',', 'then']
de_morgen_expression = 'neither'

pluralism_keywords = ['all', 'some', 'no', 'therefore']
individuals_keyword = ['is an', 'is a', 'is not a', 'is not an']
syllogism_keywords = pluralism_keywords + individuals_keyword

complete_negation = 'it is not the case that'
complete_negation_tokens = ['it', 'is', 'not', 'the', 'case', 'that']

# Maybe we wanna change this to be regular expressions?
