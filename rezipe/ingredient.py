from dataclasses import dataclass
from typing import Any


@dataclass
class Ingredient:
    name: str
    amount: Any