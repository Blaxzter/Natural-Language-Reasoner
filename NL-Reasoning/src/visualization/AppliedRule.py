"""
Data class that just encapsulates the applied rule
"""
from dataclasses import dataclass, field
from typing import Dict, List

from logics.senteces.Expression import Expression


@dataclass()
class AppliedRule:
    rule_name: str = field()
    referenced_line: int = field()
    c_expression: Expression = field(default = None, compare = False, hash = False)
    matched_expression: Expression = field(default = None, compare = False, hash = False)
    created_expressions: Dict[int, List[Expression]] = field(default = None, compare = False, hash = False)
    rule_desc_obj: Dict = field(default = None, compare = False, hash = False)

    def get_dict(self):
        """
        Return a dictionary of this applied rule
        :return: The dict representing the rule
        """
        return dict(
            rule_name = self.rule_name,
            referenced_line = self.referenced_line,
            created_expressions = None if self.created_expressions is None else str([expression for expression in self.created_expressions.values()]),
            c_expression = str(self.c_expression),
            matched_expression = str(self.matched_expression),
            rule_desc_obj = str(self.rule_desc_obj)
        )