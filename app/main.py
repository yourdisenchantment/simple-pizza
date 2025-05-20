# app/main.py

"""Главный модуль приложения."""

import os

from app.core.config import DB_PATH, DATA_DIR
from app.ui.main_menu import show_main_menu


def check_database() -> bool:
    """Проверить существование базы данных.

    Returns:
        True если база существует, False если нужно создать
    """
    return os.path.exists(DB_PATH)


def initialize_database() -> None:
    """Инициализировать базу данных."""
    try:
        # Создаем директорию для БД если её нет
        os.makedirs(DATA_DIR, exist_ok=True)

        # Импортируем и запускаем скрипт инициализации
        from scripts.setup_db import setup

        setup()

        print("База данных успешно инициализирована")

    except Exception as error:
        print(f"Ошибка при инициализации базы данных: {error}")
        raise


def main() -> None:
    """Точка входа в приложение."""
    try:
        # Проверяем наличие базы данных
        if not check_database():
            print("База данных не найдена")
            initialize = input("Инициализировать базу данных? (y/n): ").lower()

            if initialize == "y":
                initialize_database()
            else:
                print("Невозможно продолжить без базы данных")
                return

        # Запускаем главное меню
        show_main_menu()

    except KeyboardInterrupt:
        print("\nРабота программы завершена")
    except Exception as error:
        print(f"\nПроизошла непредвиденная ошибка: {error}")
    finally:
        print("\nДо свидания!")


if __name__ == "__main__":
    main()
