"""
Модуль, содержащий классы, представляющие данные (модели данных для пицц, ингредиентов и т.п.).
"""

from dataclasses import dataclass


@dataclass
class Pizza:
    id_pizza: int
    name_pizza: str
    is_visible: bool

    def __repr__(self):
        return (
            f"Pizza("
            f"id_pizza={self.id_pizza},"
            f"name_pizza='{self.name_pizza}',"
            f"is_visible={self.is_visible}"
            f")"
        )


@dataclass
class PizzaCost:
    id_pizza: int
    cost_factor: float

    def __repr__(self):
        return (
            f"PizzaCost("
            f"id_pizza={self.id_pizza},"
            f"cost_factor={self.cost_factor}"
            f")"
        )


@dataclass
class Ingredient:
    id_ingredient: int
    name_ingredient: str

    def __repr__(self):
        return (
            f"Ingredient("
            f"id_ingredient={self.id_ingredient},"
            f"name_ingredient={self.name_ingredient}"
            f")"
        )


@dataclass
class IngredientCost:
    id_ingredient: int
    cost: float

    def __repr__(self):
        return (
            f"IngredientCost("
            f"id_ingredient={self.id_ingredient},"
            f"cost={self.cost}"
            f")"
        )


@dataclass
class IngredientAmount:
    id_ingredient: int
    amount: int

    def __repr__(self):
        return (
            f"IngredientAmount("
            f"id_ingredient={self.id_ingredient},"
            f"amount={self.amount}"
            f")"
        )


@dataclass
class Recipe:
    id_pizza: int
    id_ingredient: int
    amount: int

    def __repr__(self):
        return (
            f"Recipe("
            f"id_pizza={self.id_pizza},"
            f"id_ingredient='{self.id_ingredient}',"
            f"amount={self.amount}"
            f")"
        )
