# scripts/setup_db.py

"""Скрипт для создания и инициализации базы данных SQLite."""

from app.db.connection import get_connection
from app.db.queries import *
from app.db.schema import create_tables, drop_tables


def seed_initial_data(conn: sqlite3.Connection) -> None:
    """Создаёт 2 пиццы с нужными ингредиентами.

    Args:
        conn: Соединение с базой данных

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    # ---------------- Пиццы ----------------
    margherita_id = create_pizza("Маргарита", visible=True, conn=conn)
    pepperoni_id = create_pizza("Пепперони", visible=True, conn=conn)

    set_pizza_cost(margherita_id, 1.0, conn=conn)
    set_pizza_cost(pepperoni_id, 1.3, conn=conn)

    # ---------------- Ингредиенты ----------------
    dough_id = create_ingredient("Тесто", conn=conn)
    cheese_id = create_ingredient("Сыр", conn=conn)
    salami_id = create_ingredient("Салями", conn=conn)
    tomato_id = create_ingredient("Томатная основа", conn=conn)
    cream_id = create_ingredient("Сливочная основа", conn=conn)  # запасной

    # ---------------- Цены ингредиентов ----------------
    set_ingredient_cost(dough_id, 0.8, conn=conn)
    set_ingredient_cost(cheese_id, 0.5, conn=conn)
    set_ingredient_cost(salami_id, 0.7, conn=conn)
    set_ingredient_cost(tomato_id, 0.3, conn=conn)
    set_ingredient_cost(cream_id, 0.4, conn=conn)

    # ---------------- Рецепт Маргариты ----------------
    upsert_recipe_item(margherita_id, dough_id, 1, conn=conn)
    upsert_recipe_item(margherita_id, cheese_id, 2, conn=conn)
    upsert_recipe_item(margherita_id, tomato_id, 1, conn=conn)

    # ---------------- Рецепт Пепперони ----------------
    upsert_recipe_item(pepperoni_id, dough_id, 1, conn=conn)
    upsert_recipe_item(pepperoni_id, cheese_id, 2, conn=conn)
    upsert_recipe_item(pepperoni_id, tomato_id, 1, conn=conn)
    upsert_recipe_item(pepperoni_id, salami_id, 2, conn=conn)

    # ---------------- Наполнение ингредиентов ----------------
    set_ingredient_amount(dough_id, 100, conn=conn)
    set_ingredient_amount(cheese_id, 100, conn=conn)
    set_ingredient_amount(salami_id, 50, conn=conn)
    set_ingredient_amount(tomato_id, 80, conn=conn)
    set_ingredient_amount(cream_id, 60, conn=conn)


def setup() -> None:
    """Полный сброс и наполнение базы данных."""
    try:
        with get_connection() as conn:
            print("Удаление старых таблиц...")
            drop_tables(conn)

            print("Создание схемы...")
            create_tables(conn)

            print("Загрузка начальных данных...")
            seed_initial_data(conn)

        print("База данных успешно инициализирована!")
    except Exception as error:
        print(f"Ошибка при инициализации базы данных: {error}")
        raise


if __name__ == "__main__":
    setup()
