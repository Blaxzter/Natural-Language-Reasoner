from typing import Any, Dict, List, Tuple

from logics.senteces.Expression import Expression

class Rule:

    def get_explanation(self) -> Dict[Any, Tuple[str, list, List[list]]]:
        pass

    def apply_rule(self, clause: Expression, *args):
        pass