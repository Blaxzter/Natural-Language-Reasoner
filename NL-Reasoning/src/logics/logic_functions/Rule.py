from typing import Any, Dict, List, Tuple
from logics.senteces.Expression import Expression
import abc


class Rule(metaclass=abc.ABCMeta):
    """
    Rule parent class from which all rule explanation classes have to inherit
    """

    def get_explanation(self) -> Dict[Any, Tuple[str, list, List[list]]]:
        """
        :return: Create the explanation based on the provided data in the object.
        """
        pass
