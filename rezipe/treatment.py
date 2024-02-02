
from typing import Any, ParamSpec, Self, TypeVar
from pint import Unit, Quantity
from dataclasses import dataclass
from rezipe.ingredient import Ingredient, IngredientGroup
from autoname import AutoName, auto
T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")
T = TypeVar("T")


@dataclass
class GenericTreatment:
    name: str
    duration: Quantity | None = None
    temperature: Quantity | None = None
    notes: str | None = None

    def __init__(self, name, *, duration= None, temperature= None, notes = None,**kwargs) -> None:
        self.name = name
        self.duration = duration
        self.temperature = temperature
        self.notes = notes
        self.__dict__.update(kwargs)

    
        
    def __call__(self, *args: Ingredient | IngredientGroup, **kwds: Any) -> Any:
        # convert to IngredientGroup
        ig = IngredientGroup()
        for arg in args:
            match arg:
                case Ingredient | IngredientGroup:
                    ig += arg
                case Quantity:
                    if arg.units == Unit('g'):
                        s
            ig += arg

        return 

@dataclass
class IngredientGroupWithTreatment(GenericTreatment):
    ingredients: list[Ingredient | IngredientGroup | Self]

    def __init__(self, name, ingredients, *, duration= None, temperature= None, notes = None,**kwargs) -> None:
        super().__init__(name, duration=duration, temperature=temperature, notes=notes)
        self.ingredients = ingredients

    def __call__(self, *args: Ingredient | IngredientGroup, **kwds: Any) -> Any:
        pass