from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional, List
from typeguard import typechecked, check_type


def make_rasd() -> Dict[str, List[int]]:
    return {}


@dataclass
class a:
    _obstacles: Dict[str, List[int]] = field(default_factory=make_rasd)  # ok
