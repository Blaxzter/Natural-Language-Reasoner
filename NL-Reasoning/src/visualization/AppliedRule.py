from dataclasses import dataclass, field
from typing import List

from src.logics.Expression import Expression


@dataclass()
class AppliedRule:
    rule_name: str = field()
    referenced_line: int = field()
    c_expression: Expression = field(default = None, compare = False, hash = False)
    matched_expression: Expression = field(default = None, compare = False, hash = False)
    created_expressions: List[Expression] = field(default = None, compare = False, hash = False)

    def get_dict(self):
        return dict(
            rule_name = self.rule_name,
            referenced_line = self.referenced_line,
            created_expressions = str(self.c_expression),
            c_expression = str(self.matched_expression),
            matched_expression = str(self.created_expressions),
        )