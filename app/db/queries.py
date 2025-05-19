"""Модуль, содержащий SQL-запросы для выполнения различных операций с базой данных.
"""

from typing import List, Optional

from app.core.models import *
from app.db.connection import get_connection

# ---------------- PIZZA ----------------

SQL_SELECT_ALL_PIZZAS = """
                        SELECT id_pizza, name_pizza, is_visible
                        FROM pizza
                        WHERE is_visible = 1; \
                        """
SQL_SELECT_PIZZA_BY_ID = """
                         SELECT id_pizza, name_pizza, is_visible
                         FROM pizza
                         WHERE id_pizza = ?; \
                         """
SQL_INSERT_PIZZA = """
                   INSERT INTO pizza(name_pizza, is_visible)
                   VALUES (?, ?); \
                   """
SQL_UPDATE_PIZZA_VISIBILITY = """
                              UPDATE pizza
                              SET is_visible = ?
                              WHERE id_pizza = ?; \
                              """
SQL_DELETE_PIZZA = """
                   DELETE
                   FROM pizza
                   WHERE id_pizza = ?; \
                   """


def get_all_pizzas() -> List[Pizza]:
    """Получить список видимых пицц.

    Returns:
        List[Pizza]: список объектов Pizza
    """
    try:
        with get_connection() as conn:
            rows = conn.execute(SQL_SELECT_ALL_PIZZAS).fetchall()
            return [Pizza(**row) for row in rows]

    except Exception as error:
        print(f"Ошибка при получении всех пицц: {error}")
        return []

def get_pizza_by_id(pizza_id: int) -> Optional[Pizza]:
    """Найти пиццу по её ID.

    Args:
        pizza_id (int): идентификатор пиццы

    Returns:
        Pizza | None: объект Pizza или None, если не найдено
    """
    try:
        with get_connection() as conn:
            row = conn.execute(SQL_SELECT_PIZZA_BY_ID, (pizza_id,)).fetchone()
            return Pizza(**row) if row else None

    except Exception as error:
        print(f"Ошибка при получении пиццы по ID: {error}")
        return None


def create_pizza(name: str, visible: bool = True) -> int:
    """Создать новую пиццу.

    Args:
        name (str): название пиццы
        visible (bool): флаг видимости (по умолчанию True)

    Returns:
        int: новосозданный id_pizza
    """
    try:
        with get_connection() as conn:
            cur = conn.execute(SQL_INSERT_PIZZA, (name, int(visible)))
            conn.commit()
            return cur.lastrowid

    except Exception as error:
        print(f"Ошибка при создании пиццы: {error}")
        return -1


def update_pizza_visibility(pizza_id: int, visible: bool) -> None:
    """Изменить флаг is_visible для пиццы.

    Args:
        pizza_id (int): идентификатор пиццы
        visible (bool): новый флаг видимости
    """
    try:
        with get_connection() as conn:
            conn.execute(SQL_UPDATE_PIZZA_VISIBILITY, (int(visible), pizza_id))
            conn.commit()

    except Exception as error:
        print(f"Ошибка при обновлении видимости пиццы: {error}")


def delete_pizza(pizza_id: int) -> None:
    """Удалить пиццу из базы.

    Args:
        pizza_id (int): идентификатор удаляемой пиццы
    """
    try:
        with get_connection() as conn:
            conn.execute(SQL_DELETE_PIZZA, (pizza_id,))
            conn.commit()
    except Exception as error:
        print(f"Ошибка при удалении пиццы: {error}")


# ---------------- PIZZA COST ----------------

SQL_SELECT_PIZZA_COST = """
                        SELECT id_pizza, cost_factor
                        FROM pizza_cost
                        WHERE id_pizza = ?;
"""
SQL_UPSERT_PIZZA_COST = """
    INSERT OR REPLACE INTO pizza_cost(id_pizza, cost_factor)
    VALUES (?, ?);
"""


def get_pizza_cost(pizza_id: int) -> Optional[PizzaCost]:
    """Вытащить множитель стоимости для конкретной пиццы.

    Args:
        pizza_id (int): идентификатор пиццы

    Returns:
        PizzaCost | None: объект PizzaCost или None
    """
    try:
        base_cost = get_pizza_base_cost(pizza_id)
        with get_connection() as conn:
            row = conn.execute(SQL_SELECT_PIZZA_COST, (pizza_id,)).fetchone()
            if row:
                cost_factor = row["cost_factor"]
                return base_cost * cost_factor
            return None

    except Exception as error:
        print(f"Ошибка при получении полной стоимости пиццы: {error}")
        return None


def set_pizza_cost(pizza_id: int, cost_factor: float) -> None:
    """Установить или обновить множитель стоимости пиццы.

    Args:
        pizza_id (int): идентификатор пиццы
        cost_factor (float): новый множитель стоимости
    """
    with get_connection() as conn:
        conn.execute(SQL_UPSERT_PIZZA_COST, (pizza_id, cost_factor))
        conn.commit()


# ---------------- INGREDIENT ----------------

SQL_SELECT_ALL_INGREDIENTS = """
                             SELECT id_ingredient, name_ingredient
                             FROM ingredient; \
                             """
SQL_SELECT_INGREDIENT_BY_ID = """
                              SELECT id_ingredient, name_ingredient
                              FROM ingredient
                              WHERE id_ingredient = ?; \
                              """
SQL_INSERT_INGREDIENT = """
                        INSERT INTO ingredient(name_ingredient)
                        VALUES (?); \
                        """
SQL_DELETE_INGREDIENT = """
                        DELETE
                        FROM ingredient
                        WHERE id_ingredient = ?; \
                        """


def get_all_ingredients() -> List[Ingredient]:
    """Список всех ингредиентов.

    Returns:
        List[Ingredient]: все записи из ingredient
    """
    with get_connection() as conn:
        rows = conn.execute(SQL_SELECT_ALL_INGREDIENTS).fetchall()
        return [Ingredient(**row) for row in rows]


def get_ingredient_by_id(ingredient_id: int) -> Optional[Ingredient]:
    """Найти ингредиент по ID.

    Args:
        ingredient_id (int): идентификатор ингредиента

    Returns:
        Ingredient | None: объект Ingredient или None
    """
    with get_connection() as conn:
        row = conn.execute(SQL_SELECT_INGREDIENT_BY_ID, (ingredient_id,)).fetchone()
        return Ingredient(**row) if row else None


def create_ingredient(name: str) -> int:
    """Добавить новый ингредиент.

    Args:
        name (str): название ингредиента

    Returns:
        int: сгенерированный id_ingredient
    """
    with get_connection() as conn:
        cur = conn.execute(SQL_INSERT_INGREDIENT, (name,))
        conn.commit()
        return cur.lastrowid


def delete_ingredient(ingredient_id: int) -> None:
    """Удалить ингредиент по ID.

    Args:
        ingredient_id (int): идентификатор ингредиента
    """
    with get_connection() as conn:
        conn.execute(SQL_DELETE_INGREDIENT, (ingredient_id,))
        conn.commit()


# ---------------- INGREDIENT COST ----------------

SQL_SELECT_INGREDIENT_COST = """
                             SELECT id_ingredient, cost
                             FROM ingredient_cost
                             WHERE id_ingredient = ?; \
                             """
SQL_UPSERT_INGREDIENT_COST = """
    INSERT OR REPLACE INTO ingredient_cost(id_ingredient, cost)
    VALUES (?, ?);
"""


def get_ingredient_cost(ingredient_id: int) -> Optional[IngredientCost]:
    """Получить стоимость единицы ингредиента.

    Args:
        ingredient_id (int): идентификатор ингредиента

    Returns:
        IngredientCost | None
    """
    with get_connection() as conn:
        row = conn.execute(SQL_SELECT_INGREDIENT_COST, (ingredient_id,)).fetchone()
        return IngredientCost(**row) if row else None


def set_ingredient_cost(ingredient_id: int, cost: float) -> None:
    """Установить или обновить стоимость ингредиента.

    Args:
        ingredient_id (int): идентификатор ингредиента
        cost (float): стоимость за единицу
    """
    with get_connection() as conn:
        conn.execute(SQL_UPSERT_INGREDIENT_COST, (ingredient_id, cost))
        conn.commit()


# ---------------- INGREDIENT AMOUNT ----------------

SQL_SELECT_INGREDIENT_AMOUNT = """
                               SELECT id_ingredient, amount
                               FROM ingredient_amount
                               WHERE id_ingredient = ?; \
                               """
SQL_UPSERT_INGREDIENT_AMOUNT = """
    INSERT OR REPLACE INTO ingredient_amount(id_ingredient, amount)
    VALUES (?, ?);
"""


def get_ingredient_amount(ingredient_id: int) -> Optional[IngredientAmount]:
    """Узнать остаток ингредиента на складе.

    Args:
        ingredient_id (int): идентификатор ингредиента

    Returns:
        IngredientAmount | None
    """
    with get_connection() as conn:
        row = conn.execute(SQL_SELECT_INGREDIENT_AMOUNT, (ingredient_id,)).fetchone()
        return IngredientAmount(**row) if row else None


def set_ingredient_amount(ingredient_id: int, amount: int) -> None:
    """Установить/обновить количество ингредиента на складе.

    Args:
        ingredient_id (int): идентификатор ингредиента
        amount (int): новое количество на складе
    """
    with get_connection() as conn:
        conn.execute(SQL_UPSERT_INGREDIENT_AMOUNT, (ingredient_id, amount))
        conn.commit()


# ---------------- RECIPE ----------------

SQL_SELECT_RECIPE_BY_PIZZA = """
                             SELECT id_pizza, id_ingredient, amount
                             FROM recipe
                             WHERE id_pizza = ?; \
                             """
SQL_UPSERT_RECIPE_ITEM = """
    INSERT OR REPLACE INTO recipe(id_pizza, id_ingredient, amount)
    VALUES (?, ?, ?);
"""
SQL_DELETE_RECIPE_BY_PIZZA = """
                             DELETE
                             FROM recipe
                             WHERE id_pizza = ?; \
                             """


def get_recipe_for_pizza(pizza_id: int) -> List[Recipe]:
    """Получить рецепт (список ингредиентов с количеством) для пиццы.

    Args:
        pizza_id (int): идентификатор пиццы

    Returns:
        List[Recipe]: список объектов Recipe
    """
    with get_connection() as conn:
        rows = conn.execute(SQL_SELECT_RECIPE_BY_PIZZA, (pizza_id,)).fetchall()
        return [Recipe(**row) for row in rows]


def upsert_recipe_item(pizza_id: int, ingredient_id: int, amount: int) -> None:
    """Добавить или обновить одну строку рецепта.

    Args:
        pizza_id (int): идентификатор пиццы
        ingredient_id (int): идентификатор ингредиента
        amount (int): количество ингредиента
    """
    with get_connection() as conn:
        conn.execute(SQL_UPSERT_RECIPE_ITEM, (pizza_id, ingredient_id, amount))
        conn.commit()


def delete_recipe_for_pizza(pizza_id: int) -> None:
    """Удалить весь рецепт (все строки) для заданной пиццы.

    Args:
        pizza_id (int): идентификатор пиццы
    """
    with get_connection() as conn:
        conn.execute(SQL_DELETE_RECIPE_BY_PIZZA, (pizza_id,))
        conn.commit()


# ---------------- PIZZA COST ----------------

SQL_GET_PIZZA_BASE_COST = """
                          SELECT ic.cost, r.amount
                          FROM recipe r
                                   JOIN ingredient_cost ic ON r.id_ingredient = ic.id_ingredient
                          WHERE r.id_pizza = ? \
                          """


def get_pizza_base_cost(pizza_id: int) -> float:
    """Возвращает себестоимость пиццы (без учёта коэффициента стоимости),
    вычисленную как сумма: стоимость_ингредиента * количество_ингредиента.

    Args:
        pizza_id (int): идентификатор пиццы

    Returns:
        float: стоимость пиццы
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL_GET_PIZZA_BASE_COST, (pizza_id,))
    result = cursor.fetchall()
    conn.close()
    return sum(cost * amount for cost, amount in result)
