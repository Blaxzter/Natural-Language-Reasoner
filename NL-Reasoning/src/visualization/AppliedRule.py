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
