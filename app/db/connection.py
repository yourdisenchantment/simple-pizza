# app/db/connection.py

"""Модуль для управления соединением с базой данных."""

import contextlib
import sqlite3
from typing import Generator

from app.core.config import DB_PATH


@contextlib.contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Контекстный менеджер для соединения с базой данных.

    Создает соединение с БД, настраивает row_factory и автоматически закрывает соединение.

    Yields:
        Соединение с БД

    Raises:
        sqlite3.Error: При ошибке подключения к БД
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка подключения к базе данных: {error}")

    finally:
        if conn:
            try:
                conn.close()
            except sqlite3.Error:
                # Игнорируем ошибки при закрытии соединения
                pass
