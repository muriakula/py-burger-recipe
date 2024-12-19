from abc import abstractmethod, ABC
from typing import Type, Any


class Validator(ABC):
    def __set_name__(self, owner: Type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, obj: Any, obj_type: Type) -> None:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: Any, value: Any) -> None:
        if self.validate(value):
            setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if self.min_value <= value <= self.max_value:
            return True
        raise ValueError(f"Quantity should not be less than {self.min_value} "
                         f"and greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: Any) -> bool:
        if isinstance(value, str):
            if value in self.options:
                return True
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self, buns: int, cheese: int, tomatoes: int,
                 cutlets: int, eggs: int, sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
