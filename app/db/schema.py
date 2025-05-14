"""
Модуль, содержащий SQL-запросы для создания и инициализации схемы базы данных (таблицы, индексы и т.п.).
"""

import sqlite3

CREATE_PIZZA_TABLE = """
                     CREATE TABLE IF NOT EXISTS pizza
                     (
                         id_pizza
                         INTEGER
                         PRIMARY
                         KEY,
                         name_pizza
                         TEXT
                         NOT
                         NULL,
                         is_visible
                         BOOLEAN
                         NOT
                         NULL
                     ); \
                     """

CREATE_PIZZA_COST_TABLE = """
                          CREATE TABLE IF NOT EXISTS pizza_cost
                          (
                              id_pizza
                              INTEGER
                              PRIMARY
                              KEY,
                              cost_factor
                              REAL
                              NOT
                              NULL,
                              FOREIGN
                              KEY
                          (
                              id_pizza
                          ) REFERENCES pizza
                          (
                              id_pizza
                          )
                              ); \
                          """

CREATE_INGREDIENT_TABLE = """
                          CREATE TABLE IF NOT EXISTS ingredient
                          (
                              id_ingredient
                              INTEGER
                              PRIMARY
                              KEY,
                              name_ingredient
                              TEXT
                              NOT
                              NULL
                          ); \
                          """

CREATE_INGREDIENT_COST_TABLE = """
                               CREATE TABLE IF NOT EXISTS ingredient_cost
                               (
                                   id_ingredient
                                   INTEGER
                                   PRIMARY
                                   KEY,
                                   cost
                                   REAL
                                   NOT
                                   NULL,
                                   FOREIGN
                                   KEY
                               (
                                   id_ingredient
                               ) REFERENCES ingredient
                               (
                                   id_ingredient
                               )
                                   ); \
                               """

CREATE_INGREDIENT_AMOUNT_TABLE = """
                                 CREATE TABLE IF NOT EXISTS ingredient_amount
                                 (
                                     id_ingredient
                                     INTEGER
                                     PRIMARY
                                     KEY,
                                     amount
                                     INTEGER
                                     NOT
                                     NULL,
                                     FOREIGN
                                     KEY
                                 (
                                     id_ingredient
                                 ) REFERENCES ingredient
                                 (
                                     id_ingredient
                                 )
                                     ); \
                                 """

CREATE_RECIPE_TABLE = """
                      CREATE TABLE IF NOT EXISTS recipe
                      (
                          id_pizza
                          INTEGER
                          NOT
                          NULL,
                          id_ingredient
                          INTEGER
                          NOT
                          NULL,
                          amount
                          INTEGER
                          NOT
                          NULL,
                          FOREIGN
                          KEY
                      (
                          id_pizza
                      ) REFERENCES pizza
                      (
                          id_pizza
                      ),
                          FOREIGN KEY
                      (
                          id_ingredient
                      ) REFERENCES ingredient
                      (
                          id_ingredient
                      ),
                          PRIMARY KEY
                      (
                          id_pizza,
                          id_ingredient
                      )
                          ); \
                      """


def create_tables(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_PIZZA_TABLE)
        cursor.execute(CREATE_PIZZA_COST_TABLE)
        cursor.execute(CREATE_INGREDIENT_TABLE)
        cursor.execute(CREATE_INGREDIENT_COST_TABLE)
        cursor.execute(CREATE_INGREDIENT_AMOUNT_TABLE)
        cursor.execute(CREATE_RECIPE_TABLE)
        conn.commit()
        print("Таблицы успешно созданы")
    except sqlite3.Error as error:
        print(f"Ошибка создания таблиц: {error}")
        conn.rollback()


def drop_tables(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS recipe")
        cursor.execute("DROP TABLE IF EXISTS ingredient_amount")
        cursor.execute("DROP TABLE IF EXISTS ingredient_cost")
        cursor.execute("DROP TABLE IF EXISTS ingredient")
        cursor.execute("DROP TABLE IF EXISTS pizza_cost")
        cursor.execute("DROP TABLE IF EXISTS pizza")
        cursor.execute("DROP TABLE IF EXISTS sqlite_sequence")
        conn.commit()
        print("Таблицы успешно удалены")
    except sqlite3.Error as error:
        print(f"Ошибка удаления таблиц: {error}")
        conn.rollback()
