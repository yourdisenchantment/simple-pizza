# app/core/models.py

"""Модуль, содержащий классы, представляющие данные (модели данных для пицц, ингредиентов и т.п.)."""

from dataclasses import dataclass


@dataclass
class Pizza:
    """Модель пиццы."""

    id_pizza: int
    name_pizza: str
    is_visible: bool

    def __str__(self) -> str:
        return f"Пицца '{self.name_pizza}' (ID: {self.id_pizza})"


@dataclass
class PizzaCost:
    """Модель стоимости пиццы."""

    id_pizza: int
    cost_factor: float

    def __str__(self) -> str:
        return f"Множитель стоимости пиццы {self.id_pizza}: {self.cost_factor}"


@dataclass
class Ingredient:
    """Модель ингредиента."""

    id_ingredient: int
    name_ingredient: str

    def __str__(self) -> str:
        return f"Ингредиент '{self.name_ingredient}' (ID: {self.id_ingredient})"


@dataclass
class IngredientCost:
    """Модель стоимости ингредиента."""

    id_ingredient: int
    cost: float

    def __str__(self) -> str:
        return f"Стоимость ингредиента {self.id_ingredient}: {self.cost}"


@dataclass
class IngredientAmount:
    """Модель количества ингредиента на складе."""

    id_ingredient: int
    amount: int

    def __str__(self) -> str:
        return f"Количество ингредиента {self.id_ingredient}: {self.amount}"


@dataclass
class Recipe:
    """Модель записи в рецепте пиццы."""

    id_pizza: int
    id_ingredient: int
    amount: int

    def __str__(self) -> str:
        return f"Ингредиент {self.id_ingredient} в пицце {self.id_pizza}: {self.amount} шт."
