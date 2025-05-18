"""Модуль, содержащий настройки приложения (путь к базе данных и другие параметры).
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_NAME = "pizzeria.db"
DB_PATH = os.path.join(BASE_DIR, "data", DB_NAME)
