from logics.logic_functions.AndRule import AndRule
from logics.logic_functions.DeMorganRule import DeMorganRule
from logics.logic_functions.OrRule import OrRule
from logics.logic_functions.QuantificationRule import QuantificationRule
from logics.logic_functions.SyllogismRule import SyllogismRule
from logics.logic_functions.WhenRule import WhenRule

# Order is important, try to not branch to early
rule_set = dict(
    and_rule = AndRule.apply_rule,
    de_Morgan_Law = DeMorganRule.apply_rule,
    or_rule = OrRule.apply_rule,
    when_rule = WhenRule.apply_rule,

    syllogism_reverse_rule = SyllogismRule.apply_reverse,
    syllogism_rule_1 = SyllogismRule.apply_rule1,
    syllogism_rule_2 = SyllogismRule.apply_rule2,
    syllogism_rule_3 = SyllogismRule.apply_rule3,

    quantification_negation_rule = QuantificationRule.negation_apply_rule,
    quantification_replace_rule = QuantificationRule.apply_replace_rule,
)


