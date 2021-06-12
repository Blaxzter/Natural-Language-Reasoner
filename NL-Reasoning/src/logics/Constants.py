separator = ' '
negation_keywords = ['not', 'never']
connection_keywords = ['or', 'and', ';']
when_keywords = ['when', 'if']
when_split_tokens = [',', 'then']

# todo because
# todo regex

de_morgen_expression = 'neither'

syllogism_regex = "/(All|Some|No) [a-zA-Z -]+ (have|are not|are|is not a|is not an|is an|is a|is) [a-zA-Z -]+/gmi"
pluralism_keywords = ['all', 'some', 'no', 'therefore']
individuals_keywords = ['is an', 'is a', 'is not a', 'is not an']
syllogism_keywords = pluralism_keywords + individuals_keywords

complete_negation = 'it is not the case that'
complete_negation_tokens = ['it', 'is', 'not', 'the', 'case', 'that']

quantified_keywords_plural = ['for each', 'for all']
quantified_keywords_singular = ['there is a ', 'it exists a']
quantified_keywords = quantified_keywords_plural + quantified_keywords_singular

# Maybe we wanna change this to be regular expressions?
