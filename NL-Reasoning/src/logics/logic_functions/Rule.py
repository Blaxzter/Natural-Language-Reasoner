from typing import Any, Dict, List, Tuple
from logics.senteces.Expression import Expression
import abc

class Rule(metaclass=abc.ABCMeta):

    def get_explanation(self, applied_rule) -> Dict[Any, Tuple[str, list, List[list]]]:
        pass

    def apply_rule(self, clause: Expression, *args):
        pass
