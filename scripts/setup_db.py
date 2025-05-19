"""Скрипт для создания и инициализации базы данных SQLite.
"""

from app.db.queries import *
from app.db.schema import create_tables, drop_tables


def seed_initial_data():
    """Создаёт 2 пиццы с нужными ингредиентами.
    """

    # ---------------- Пиццы ----------------
    margherita_id = create_pizza("Маргарита", visible=True)
    pepperoni_id = create_pizza("Пепперони", visible=True)

    set_pizza_cost(margherita_id, 1.0)
    set_pizza_cost(pepperoni_id, 1.3)

    # ---------------- Ингредиенты ----------------
    dough_id = create_ingredient("Тесто")
    cheese_id = create_ingredient("Сыр")
    salami_id = create_ingredient("Салями")
    tomato_id = create_ingredient("Томатная основа")
    cream_id = create_ingredient("Сливочная основа")  # запасной

    # ---------------- Цены ингредиентов ----------------
    set_ingredient_cost(dough_id, 0.8)
    set_ingredient_cost(cheese_id, 0.5)
    set_ingredient_cost(salami_id, 0.7)
    set_ingredient_cost(tomato_id, 0.3)
    set_ingredient_cost(cream_id, 0.4)

    # ---------------- Рецепт Маргариты ----------------
    upsert_recipe_item(margherita_id, dough_id, 1)
    upsert_recipe_item(margherita_id, cheese_id, 2)
    upsert_recipe_item(margherita_id, tomato_id, 1)

    # ---------------- Рецепт Пепперони ----------------
    upsert_recipe_item(pepperoni_id, dough_id, 1)
    upsert_recipe_item(pepperoni_id, cheese_id, 2)
    upsert_recipe_item(pepperoni_id, tomato_id, 1)
    upsert_recipe_item(pepperoni_id, salami_id, 2)

    # ---------------- Наполнение ингредиентов ----------------
    set_ingredient_amount(dough_id, 100)
    set_ingredient_amount(cheese_id, 100)
    set_ingredient_amount(salami_id, 50)
    set_ingredient_amount(tomato_id, 80)
    set_ingredient_amount(cream_id, 60)

    print("Пиццы успешно добавлены!")


def setup():
    """Полный сброс и наполнение базы данных.
    """
    with get_connection() as conn:
        print("Удаление старых таблиц...")
        drop_tables(conn)

        print("Создание схемы...")
        create_tables(conn)

    print("Загрузка начальных данных...")
    seed_initial_data()


if __name__ == "__main__":
    setup()
