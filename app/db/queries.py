# app/db/queries.py

"""Модуль, содержащий SQL-запросы для выполнения различных операций с базой данных."""

import sqlite3
from typing import List, Tuple, Optional

from app.core.config import DB_PATH
from app.core.models import *


def ensure_connection(
    conn: Optional[sqlite3.Connection] = None,
) -> Tuple[sqlite3.Connection, bool]:
    """Проверяет соединение и при необходимости создает новое.

    Args:
        conn: Соединение для проверки

    Returns:
        Tuple[sqlite3.Connection, bool]: (соединение, флаг необходимости закрытия)
    """
    if conn is None:
        new_conn = sqlite3.connect(DB_PATH)
        new_conn.row_factory = sqlite3.Row
        return new_conn, True

    try:
        conn.execute("SELECT 1").fetchone()
        return conn, False
    except (sqlite3.Error, AttributeError):
        new_conn = sqlite3.connect(DB_PATH)
        new_conn.row_factory = sqlite3.Row
        return new_conn, True


# ---------------- PIZZA ----------------

SQL_SELECT_ALL_PIZZAS = """
                        SELECT id_pizza, name_pizza, is_visible
                        FROM pizza
                        WHERE is_visible = 1;
                        """
SQL_SELECT_PIZZA_BY_ID = """
                         SELECT id_pizza, name_pizza, is_visible
                         FROM pizza
                         WHERE id_pizza = ?;
                         """
SQL_INSERT_PIZZA = """
                   INSERT INTO pizza(name_pizza, is_visible)
                   VALUES (?, ?);
                   """
SQL_UPDATE_PIZZA_VISIBILITY = """
                              UPDATE pizza
                              SET is_visible = ?
                              WHERE id_pizza = ?;
                              """
SQL_DELETE_PIZZA = """
                   DELETE
                   FROM pizza
                   WHERE id_pizza = ?;
                   """


def get_all_pizzas(conn: Optional[sqlite3.Connection] = None) -> List[Pizza]:
    """Получить список видимых пицц.

    Args:
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Список объектов Pizza

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            rows = conn.execute(SQL_SELECT_ALL_PIZZAS).fetchall()
            result = [Pizza(**row) for row in rows]

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении всех пицц: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def get_pizza_by_id(
    pizza_id: int, conn: Optional[sqlite3.Connection] = None
) -> Optional[Pizza]:
    """Найти пиццу по её ID.

    Args:
        pizza_id: Идентификатор пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Объект Pizza или None, если не найден

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            row = conn.execute(SQL_SELECT_PIZZA_BY_ID, (pizza_id,)).fetchone()
            result = Pizza(**row) if row else None

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении пиццы по ID: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def create_pizza(
    name: str, visible: bool = True, conn: Optional[sqlite3.Connection] = None
) -> int:
    """Создать новую пиццу.

    Args:
        name: Название пиццы
        visible: Флаг видимости (по умолчанию True)
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        ID созданной пиццы

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            cur = conn.execute(SQL_INSERT_PIZZA, (name, int(visible)))
            conn.commit()
            result = cur.lastrowid

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при создании пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def update_pizza_visibility(
    pizza_id: int, visible: bool, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Изменить флаг видимости для пиццы.

    Args:
        pizza_id: Идентификатор пиццы
        visible: Новый флаг видимости
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            conn.execute(SQL_UPDATE_PIZZA_VISIBILITY, (int(visible), pizza_id))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при обновлении видимости пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def delete_pizza(pizza_id: int, conn: Optional[sqlite3.Connection] = None) -> None:
    """Удалить пиццу.

    Args:
        pizza_id: Идентификатор удаляемой пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            conn.execute(SQL_DELETE_PIZZA, (pizza_id,))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при удалении пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


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
SQL_GET_PIZZA_BASE_COST = """
    SELECT ic.cost, r.amount
    FROM recipe r
    JOIN ingredient_cost ic ON r.id_ingredient = ic.id_ingredient
    WHERE r.id_pizza = ?
"""


def get_pizza_cost(
    pizza_id: int, conn: Optional[sqlite3.Connection] = None
) -> Optional[float]:
    """Получить полную стоимость пиццы с учетом множителя.

    Args:
        pizza_id: Идентификатор пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Полная стоимость пиццы или None, если не найдена

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            if get_pizza_by_id(pizza_id, conn) is None:
                return None

            base_cost = get_pizza_base_cost(pizza_id, conn)
            row = conn.execute(SQL_SELECT_PIZZA_COST, (pizza_id,)).fetchone()

            result = base_cost * row["cost_factor"] if row else None

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении стоимости пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def set_pizza_cost(
    pizza_id: int, cost_factor: float, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Установить множитель стоимости пиццы.

    Args:
        pizza_id: Идентификатор пиццы
        cost_factor: Новый множитель стоимости
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            if cost_factor < 0:
                raise ValueError("Множитель стоимости не может быть отрицательным")

            conn.execute(SQL_UPSERT_PIZZA_COST, (pizza_id, cost_factor))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при установке стоимости пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def get_pizza_base_cost(
    pizza_id: int, conn: Optional[sqlite3.Connection] = None
) -> float:
    """Рассчитать базовую стоимость пиццы (без учёта множителя).

    Вычисляется как сумма: стоимость_ингредиента * количество_ингредиента.

    Args:
        pizza_id: Идентификатор пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Базовая стоимость пиццы

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            cursor = conn.cursor()
            cursor.execute(SQL_GET_PIZZA_BASE_COST, (pizza_id,))
            result = cursor.fetchall()

            base_cost = sum(cost * amount for cost, amount in result)

            if need_to_close:
                conn.close()

            return base_cost

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при расчёте себестоимости пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


# ---------------- INGREDIENT ----------------

SQL_SELECT_ALL_INGREDIENTS = """
                             SELECT id_ingredient, name_ingredient
                             FROM ingredient;
                             """
SQL_SELECT_INGREDIENT_BY_ID = """
                              SELECT id_ingredient, name_ingredient
                              FROM ingredient
                              WHERE id_ingredient = ?;
                              """
SQL_INSERT_INGREDIENT = """
                        INSERT INTO ingredient(name_ingredient)
                        VALUES (?);
                        """
SQL_DELETE_INGREDIENT = """
                        DELETE
                        FROM ingredient
                        WHERE id_ingredient = ?;
                        """


def get_all_ingredients(conn: Optional[sqlite3.Connection] = None) -> List[Ingredient]:
    """Получить список всех ингредиентов.

    Args:
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Список объектов Ingredient

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            rows = conn.execute(SQL_SELECT_ALL_INGREDIENTS).fetchall()
            result = [Ingredient(**row) for row in rows]

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении всех ингредиентов: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def get_ingredient_by_id(
    ingredient_id: int, conn: Optional[sqlite3.Connection] = None
) -> Optional[Ingredient]:
    """Найти ингредиент по ID.

    Args:
        ingredient_id: Идентификатор ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Объект Ingredient или None, если не найден

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            row = conn.execute(SQL_SELECT_INGREDIENT_BY_ID, (ingredient_id,)).fetchone()
            result = Ingredient(**row) if row else None

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении ингредиента по ID: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def create_ingredient(name: str, conn: Optional[sqlite3.Connection] = None) -> int:
    """Добавить новый ингредиент.

    Args:
        name: Название ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        ID созданного ингредиента

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            cur = conn.execute(SQL_INSERT_INGREDIENT, (name,))
            conn.commit()
            result = cur.lastrowid

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при создании ингредиента: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def delete_ingredient(
    ingredient_id: int, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Удалить ингредиент.

    Args:
        ingredient_id: Идентификатор ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            conn.execute(SQL_DELETE_INGREDIENT, (ingredient_id,))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при удалении ингредиента: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


# ---------------- INGREDIENT COST ----------------

SQL_SELECT_INGREDIENT_COST = """
                             SELECT id_ingredient, cost
                             FROM ingredient_cost
                             WHERE id_ingredient = ?;
                             """
SQL_UPSERT_INGREDIENT_COST = """
    INSERT OR REPLACE INTO ingredient_cost(id_ingredient, cost)
    VALUES (?, ?);
"""


def get_ingredient_cost(
    ingredient_id: int, conn: Optional[sqlite3.Connection] = None
) -> Optional[IngredientCost]:
    """Получить стоимость ингредиента.

    Args:
        ingredient_id: Идентификатор ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Объект IngredientCost или None, если не найден

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            row = conn.execute(SQL_SELECT_INGREDIENT_COST, (ingredient_id,)).fetchone()
            result = IngredientCost(**row) if row else None

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении стоимости ингредиента: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def set_ingredient_cost(
    ingredient_id: int, cost: float, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Установить стоимость ингредиента.

    Args:
        ingredient_id: Идентификатор ингредиента
        cost: Стоимость за единицу
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
        ValueError: Если передана отрицательная стоимость
    """
    if cost < 0:
        raise ValueError("Стоимость ингредиента не может быть отрицательной")

    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            conn.execute(SQL_UPSERT_INGREDIENT_COST, (ingredient_id, cost))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при установке стоимости ингредиента: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


# ---------------- INGREDIENT AMOUNT ----------------

SQL_SELECT_INGREDIENT_AMOUNT = """
                               SELECT id_ingredient, amount
                               FROM ingredient_amount
                               WHERE id_ingredient = ?;
                               """
SQL_UPSERT_INGREDIENT_AMOUNT = """
    INSERT OR REPLACE INTO ingredient_amount(id_ingredient, amount)
    VALUES (?, ?);
"""


def get_ingredient_amount(
    ingredient_id: int, conn: Optional[sqlite3.Connection] = None
) -> Optional[IngredientAmount]:
    """Получить количество ингредиента на складе.

    Args:
        ingredient_id: Идентификатор ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Объект IngredientAmount или None, если не найден

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            row = conn.execute(
                SQL_SELECT_INGREDIENT_AMOUNT, (ingredient_id,)
            ).fetchone()
            result = IngredientAmount(**row) if row else None

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении количества ингредиента: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def set_ingredient_amount(
    ingredient_id: int, amount: int, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Установить количество ингредиента на складе.

    Args:
        ingredient_id: Идентификатор ингредиента
        amount: Новое количество на складе
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
        ValueError: Если передано отрицательное количество
    """
    if amount < 0:
        raise ValueError("Количество ингредиента не может быть отрицательным")

    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            conn.execute(SQL_UPSERT_INGREDIENT_AMOUNT, (ingredient_id, amount))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при установке количества ингредиента: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def adjust_ingredient_amount(
    ingredient_id: int, delta: int, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Изменить количество ингредиента на складе на заданную величину.

    Args:
        ingredient_id: Идентификатор ингредиента
        delta: Величина изменения (положительная - добавление, отрицательная - уменьшение)
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
        ValueError: Если после изменения количество станет отрицательным
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            # Получаем текущее количество
            current = get_ingredient_amount(ingredient_id, conn)
            if current is None:
                new_amount = delta if delta > 0 else 0
            else:
                new_amount = current.amount + delta

            if new_amount < 0:
                raise ValueError("Количество ингредиента не может стать отрицательным")

            # Устанавливаем новое количество
            conn.execute(SQL_UPSERT_INGREDIENT_AMOUNT, (ingredient_id, new_amount))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при изменении количества ингредиента: {error}")

    except Exception as error:
        if isinstance(error, ValueError):
            raise
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


# ---------------- RECIPE ----------------

SQL_SELECT_RECIPE_BY_PIZZA = """
                             SELECT id_pizza, id_ingredient, amount
                             FROM recipe
                             WHERE id_pizza = ?;
                             """
SQL_UPSERT_RECIPE_ITEM = """
    INSERT OR REPLACE INTO recipe(id_pizza, id_ingredient, amount)
    VALUES (?, ?, ?);
"""
SQL_DELETE_RECIPE_BY_PIZZA = """
                             DELETE
                             FROM recipe
                             WHERE id_pizza = ?;
                             """
SQL_SELECT_ALL_RECIPES = """
    SELECT id_pizza, id_ingredient, amount
    FROM recipe;
"""


def get_recipe_for_pizza(
    pizza_id: int, conn: Optional[sqlite3.Connection] = None
) -> List[Recipe]:
    """Получить рецепт пиццы.

    Args:
        pizza_id: Идентификатор пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Список объектов Recipe (ингредиенты с их количеством)

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            rows = conn.execute(SQL_SELECT_RECIPE_BY_PIZZA, (pizza_id,)).fetchall()
            result = [Recipe(**row) for row in rows]

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении рецепта пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def upsert_recipe_item(
    pizza_id: int,
    ingredient_id: int,
    amount: int,
    conn: Optional[sqlite3.Connection] = None,
) -> None:
    """Добавить или обновить ингредиент в рецепте.

    Args:
        pizza_id: Идентификатор пиццы
        ingredient_id: Идентификатор ингредиента
        amount: Количество ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
        ValueError: Если передано отрицательное количество
    """
    if amount < 0:
        raise ValueError("Количество ингредиента в рецепте не может быть отрицательным")

    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            # Проверяем существование пиццы и ингредиента
            pizza = get_pizza_by_id(pizza_id, conn)
            ingredient = get_ingredient_by_id(ingredient_id, conn)

            if pizza is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")
            if ingredient is None:
                raise ValueError(f"Ингредиент с ID {ingredient_id} не найден")

            conn.execute(SQL_UPSERT_RECIPE_ITEM, (pizza_id, ingredient_id, amount))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при обновлении рецепта: {error}")

    except Exception as error:
        if isinstance(error, ValueError):
            raise
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def delete_recipe_item(
    pizza_id: int, ingredient_id: int, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Удалить ингредиент из рецепта.

    Args:
        pizza_id: Идентификатор пиццы
        ingredient_id: Идентификатор ингредиента
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            conn.execute(
                "DELETE FROM recipe WHERE id_pizza = ? AND id_ingredient = ?",
                (pizza_id, ingredient_id),
            )
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при удалении ингредиента из рецепта: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def delete_recipe_for_pizza(
    pizza_id: int, conn: Optional[sqlite3.Connection] = None
) -> None:
    """Удалить весь рецепт пиццы.

    Args:
        pizza_id: Идентификатор пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            if get_pizza_by_id(pizza_id, conn) is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")

            conn.execute(SQL_DELETE_RECIPE_BY_PIZZA, (pizza_id,))
            conn.commit()

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при удалении рецепта пиццы: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def check_recipe_ingredients_available(
    pizza_id: int, conn: Optional[sqlite3.Connection] = None
) -> bool:
    """Проверить наличие всех ингредиентов для приготовления пиццы.

    Args:
        pizza_id: Идентификатор пиццы
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        True если всех ингредиентов достаточно, False иначе

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            recipe_items = get_recipe_for_pizza(pizza_id, conn)

            for item in recipe_items:
                amount = get_ingredient_amount(item.id_ingredient, conn)
                if amount is None or amount.amount < item.amount:
                    return False

            if need_to_close:
                conn.close()

            return True

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при проверке наличия ингредиентов: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def get_all_recipes(conn: Optional[sqlite3.Connection] = None) -> List[Recipe]:
    """Получить все рецепты из базы данных.

    Args:
        conn: Соединение с базой данных. Если None или невалидное - создается новое.

    Returns:
        Список всех рецептов

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            rows = conn.execute(SQL_SELECT_ALL_RECIPES).fetchall()
            result = [Recipe(**row) for row in rows]

            if need_to_close:
                conn.close()

            return result

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при получении всех рецептов: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


# ---------------- ADDITION ----------------
def update_pizzas_visibility_by_ingredients(
    conn: Optional[sqlite3.Connection] = None,
) -> None:
    """Обновить видимость всех пицц на основе наличия ингредиентов.

    Проверяет наличие всех необходимых ингредиентов для каждой пиццы.
    Если хотя бы одного ингредиента из рецепта нет на складе (количество = 0),
    пицца становится невидимой для клиентов.

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        conn, need_to_close = ensure_connection(conn)

        try:
            # Получаем все ингредиенты с нулевым количеством
            all_ingredients = get_all_ingredients(conn)
            zero_ingredients = set()

            for ingredient in all_ingredients:
                amount = get_ingredient_amount(ingredient.id_ingredient, conn)
                if amount is None or amount.amount == 0:
                    zero_ingredients.add(ingredient.id_ingredient)

            if not zero_ingredients:
                return

            # Получаем все пиццы
            all_pizzas = get_all_pizzas(conn)

            # Проверяем каждую пиццу
            for pizza in all_pizzas:
                recipe = get_recipe_for_pizza(pizza.id_pizza, conn)
                should_be_visible = True

                # Если хотя бы один ингредиент с нулевым количеством, скрываем пиццу
                for item in recipe:
                    if item.id_ingredient in zero_ingredients:
                        should_be_visible = False
                        break

                # Обновляем видимость если нужно
                if pizza.is_visible != should_be_visible:
                    update_pizza_visibility(pizza.id_pizza, should_be_visible, conn)

            if need_to_close:
                conn.close()

        except sqlite3.Error as error:
            if need_to_close:
                conn.close()
            raise sqlite3.Error(f"Ошибка при обновлении видимости пицц: {error}")

    except Exception as error:
        raise sqlite3.Error(f"Ошибка при работе с БД: {error}")
