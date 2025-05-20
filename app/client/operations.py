# app/client/operations.py

"""Модуль, содержащий операции клиента для работы с пиццерией."""

from app.db.connection import get_connection
from app.db.queries import *


def get_available_pizzas() -> List[Tuple[Pizza, float]]:
    """Получить список доступных пицц с ценами.

    Returns:
        Список кортежей (пицца, цена)

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            pizzas = get_all_pizzas(conn)  # Получаем только видимые пиццы
            result = []

            for pizza in pizzas:
                price = get_pizza_cost(pizza.id_pizza, conn)
                if price is not None:  # Пропускаем пиццы без цены
                    result.append((pizza, price))

            return result

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при получении списка пицц: {error}")


def get_pizza_details(
    pizza_id: int,
) -> Tuple[Pizza, List[Tuple[Ingredient, int]], float]:
    """Получить детальную информацию о пицце.

    Args:
        pizza_id: ID пиццы

    Returns:
        Кортеж (пицца, список пар (ингредиент, количество), цена)

    Raises:
        ValueError: Если пицца не найдена или недоступна
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            # Получаем пиццу
            pizza = get_pizza_by_id(pizza_id, conn)
            if pizza is None or not pizza.is_visible:
                raise ValueError(f"Пицца не найдена или недоступна")

            # Получаем рецепт
            recipe = get_recipe_for_pizza(pizza_id, conn)
            ingredients = []

            # Получаем информацию об ингредиентах
            for item in recipe:
                ingredient = get_ingredient_by_id(item.id_ingredient, conn)
                if ingredient:
                    ingredients.append((ingredient, item.amount))

            # Получаем цену
            price = get_pizza_cost(pizza_id, conn)
            if price is None:
                raise ValueError("Невозможно рассчитать стоимость пиццы")

            return pizza, ingredients, price

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при получении информации о пицце: {error}")


def order_pizza(pizza_id: int) -> bool:
    """Заказать пиццу (списать ингредиенты).

    Args:
        pizza_id: ID пиццы

    Returns:
        True если заказ успешно выполнен

    Raises:
        ValueError: Если пицца не найдена, недоступна или недостаточно ингредиентов
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            # Проверяем существование и доступность пиццы
            pizza = get_pizza_by_id(pizza_id, conn)
            if pizza is None or not pizza.is_visible:
                raise ValueError(f"Пицца не найдена или недоступна")

            # Проверяем наличие ингредиентов
            if not check_recipe_ingredients_available(pizza_id, conn):
                raise ValueError("Недостаточно ингредиентов для приготовления пиццы")

            # Получаем рецепт
            recipe = get_recipe_for_pizza(pizza_id, conn)

            # Списываем ингредиенты
            for item in recipe:
                current = get_ingredient_amount(item.id_ingredient, conn)
                if current is None:
                    raise ValueError(
                        f"Ошибка при получении количества ингредиента {item.id_ingredient}"
                    )

                new_amount = current.amount - item.amount
                set_ingredient_amount(item.id_ingredient, new_amount, conn)

            # Обновляем видимость пицц
            update_pizzas_visibility_by_ingredients(conn)

            return True

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при оформлении заказа: {error}")
