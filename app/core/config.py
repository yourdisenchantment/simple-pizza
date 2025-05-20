# app/core/config.py

"""Модуль, содержащий настройки приложения (путь к базе данных и другие параметры)."""

from pathlib import Path
from typing import Final


# Пути
BASE_DIR: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = BASE_DIR / "data"
DB_NAME: Final[str] = "pizzeria.db"
DB_PATH: Final[Path] = DATA_DIR / DB_NAME

# Создаем директорию для данных, если её нет
DATA_DIR.mkdir(exist_ok=True)

# Настройки БД
DB_TIMEOUT: Final[float] = 5.0  # таймаут подключения к БД в секундах
DB_JOURNAL_MODE: Final[str] = "WAL"  # режим журналирования
DB_FOREIGN_KEYS: Final[bool] = True  # проверка внешних ключей

# Настройки приложения
DEFAULT_COST_FACTOR: Final[float] = 1.0  # множитель стоимости по умолчанию
MIN_INGREDIENT_AMOUNT: Final[int] = 0  # минимальное количество ингредиента
