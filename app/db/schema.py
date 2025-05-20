# app/db/schema.py

"""Модуль, содержащий SQL-запросы для создания и инициализации схемы базы данных (таблицы, индексы и т.п.)."""

import sqlite3

CREATE_PIZZA_TABLE = """
                     CREATE TABLE IF NOT EXISTS pizza (
                                                          id_pizza INTEGER PRIMARY KEY,
                                                          name_pizza TEXT NOT NULL,
                                                          is_visible BOOLEAN NOT NULL
                     ); \
                     """

CREATE_PIZZA_COST_TABLE = """
                          CREATE TABLE IF NOT EXISTS pizza_cost (
                                                                    id_pizza INTEGER PRIMARY KEY,
                                                                    cost_factor REAL NOT NULL,
                                                                    FOREIGN KEY (id_pizza) REFERENCES pizza (id_pizza)
                              ); \
                          """

CREATE_INGREDIENT_TABLE = """
                          CREATE TABLE IF NOT EXISTS ingredient (
                                                                    id_ingredient INTEGER PRIMARY KEY,
                                                                    name_ingredient TEXT NOT NULL
                          ); \
                          """

CREATE_INGREDIENT_COST_TABLE = """
                               CREATE TABLE IF NOT EXISTS ingredient_cost (
                                                                              id_ingredient INTEGER PRIMARY KEY,
                                                                              cost REAL NOT NULL,
                                                                              FOREIGN KEY (id_ingredient) REFERENCES ingredient (id_ingredient)
                                   ); \
                               """

CREATE_INGREDIENT_AMOUNT_TABLE = """
                                 CREATE TABLE IF NOT EXISTS ingredient_amount (
                                                                                  id_ingredient INTEGER PRIMARY KEY,
                                                                                  amount INTEGER NOT NULL,
                                                                                  FOREIGN KEY (id_ingredient) REFERENCES ingredient (id_ingredient)
                                     ); \
                                 """

CREATE_RECIPE_TABLE = """
                      CREATE TABLE IF NOT EXISTS recipe (
                                                            id_pizza INTEGER NOT NULL,
                                                            id_ingredient INTEGER NOT NULL,
                                                            amount INTEGER NOT NULL,
                                                            FOREIGN KEY (id_pizza) REFERENCES pizza (id_pizza),
                          FOREIGN KEY (id_ingredient) REFERENCES ingredient (id_ingredient),
                          PRIMARY KEY (id_pizza, id_ingredient)
                          ); \
                      """

DROP_TABLES_QUERIES = [
    "DROP TABLE IF EXISTS recipe",
    "DROP TABLE IF EXISTS ingredient_amount",
    "DROP TABLE IF EXISTS ingredient_cost",
    "DROP TABLE IF EXISTS ingredient",
    "DROP TABLE IF EXISTS pizza_cost",
    "DROP TABLE IF EXISTS pizza",
    "DROP TABLE IF EXISTS sqlite_sequence",
]

CREATE_TABLES_QUERIES = [
    CREATE_PIZZA_TABLE,
    CREATE_PIZZA_COST_TABLE,
    CREATE_INGREDIENT_TABLE,
    CREATE_INGREDIENT_COST_TABLE,
    CREATE_INGREDIENT_AMOUNT_TABLE,
    CREATE_RECIPE_TABLE,
]


def create_tables(conn: sqlite3.Connection) -> None:
    """Создает все необходимые таблицы в базе данных.

    Args:
        conn: Соединение с базой данных

    Raises:
        sqlite3.Error: При ошибке создания таблиц
    """
    try:
        cursor = conn.cursor()

        for query in CREATE_TABLES_QUERIES:
            cursor.execute(query)

        conn.commit()

    except sqlite3.Error as error:
        conn.rollback()
        raise sqlite3.Error(f"Ошибка создания таблиц: {error}")


def drop_tables(conn: sqlite3.Connection) -> None:
    """Удаляет все таблицы из базы данных.

    Args:
        conn: Соединение с базой данных

    Raises:
        sqlite3.Error: При ошибке удаления таблиц
    """
    try:
        cursor = conn.cursor()

        for query in DROP_TABLES_QUERIES:
            cursor.execute(query)

        conn.commit()

    except sqlite3.Error as error:
        conn.rollback()
        raise sqlite3.Error(f"Ошибка удаления таблиц: {error}")
