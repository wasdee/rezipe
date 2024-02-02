from decimal import Decimal
import marvin
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class Goods:
    name: str
    price_per_unit: Decimal | None = None
    notes: str | None = None
    source: str | None = None
