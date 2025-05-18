"""Модуль для управления соединением с базой данных.
"""

import contextlib
import sqlite3

from app.core.config import DB_PATH


@contextlib.contextmanager
def get_connection():
    """Контекстный менеджер для соединения с базой данных.

    Yields:
        sqlite3.Connection: Соединение с БД.

    Raises:
        sqlite3.Error: Если подключение не удалось.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn

    except sqlite3.Error as error:
        print(f"Ошибка подключения к базе данных: {error}")
        raise

    finally:
        if conn:
            conn.close()
