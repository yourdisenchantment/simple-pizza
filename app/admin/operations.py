# app/admin/operations.py

"""Модуль, содержащий операции администратора для управления пиццерией."""

from typing import Set

from app.db.connection import get_connection
from app.db.queries import *


# ======================== Операции с ингредиентами ========================


def add_ingredient(name: str, cost: float, amount: int = 0) -> int:
    """Добавить новый ингредиент в базу данных.

    Создает новый ингредиент, устанавливает его стоимость и начальное количество на складе.

    Args:
        name: Название ингредиента
        cost: Стоимость за единицу ингредиента
        amount: Начальное количество на складе (по умолчанию 0)

    Returns:
        ID созданного ингредиента

    Raises:
        ValueError: Если cost < 0 или amount < 0
        sqlite3.Error: При ошибке работы с БД
    """
    if cost < 0:
        raise ValueError("Стоимость ингредиента не может быть отрицательной")
    if amount < 0:
        raise ValueError("Количество ингредиента не может быть отрицательным")

    try:
        with get_connection() as conn:
            # Создаем ингредиент
            ingredient_id = create_ingredient(name, conn=conn)

            # Устанавливаем стоимость
            set_ingredient_cost(ingredient_id, cost, conn=conn)

            # Устанавливаем количество
            set_ingredient_amount(ingredient_id, amount, conn=conn)

            return ingredient_id

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при добавлении ингредиента: {error}")


def delete_ingredient(ingredient_id: int, force: bool = False) -> bool:
    """Удалить ингредиент из базы данных.

    Если ингредиент используется в рецептах и force=False, удаление не выполняется.
    Если force=True, удаляются все пиццы, использующие этот ингредиент.

    Args:
        ingredient_id: ID удаляемого ингредиента
        force: Флаг принудительного удаления вместе со всеми зависимыми пиццами

    Returns:
        True если удаление успешно, False если есть зависимые пиццы и force=False

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """

    try:
        with get_connection() as conn:  # Используем только один with
            # Проверяем существование ингредиента
            if get_ingredient_by_id(ingredient_id, conn) is None:
                raise ValueError(f"Ингредиент с ID {ingredient_id} не найден")
            # Получаем зависимые пиццы
            # dependent_pizzas = get_pizzas_with_ingredient(ingredient_id, conn)
            dependent_pizzas = get_pizzas_with_ingredient(ingredient_id)
            if dependent_pizzas and not force:
                return False
            if dependent_pizzas and force:
                # Удаляем все зависимые пиццы
                for pizza_id in dependent_pizzas:
                    delete_recipe_for_pizza(pizza_id, conn)
                    conn.execute(
                        SQL_DELETE_PIZZA, (pizza_id,)
                    )  # Прямой SQL вместо рекурсии
            # Удаляем ингредиент
            conn.execute(
                SQL_DELETE_INGREDIENT, (ingredient_id,)
            )  # Прямой SQL вместо рекурсии
            conn.commit()
            return True
    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при удалении ингредиента: {error}")


def update_ingredient_cost(ingredient_id: int, new_cost: float) -> None:
    """Изменить стоимость ингредиента.

    Args:
        ingredient_id: ID ингредиента
        new_cost: Новая стоимость за единицу ингредиента

    Raises:
        ValueError: Если new_cost < 0
        sqlite3.Error: При ошибке работы с БД
    """
    if new_cost < 0:
        raise ValueError("Стоимость ингредиента не может быть отрицательной")

    try:
        with get_connection() as conn:
            # Проверяем существование ингредиента
            if get_ingredient_by_id(ingredient_id, conn) is None:
                raise ValueError(f"Ингредиент с ID {ingredient_id} не найден")

            set_ingredient_cost(ingredient_id, new_cost, conn)

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при обновлении стоимости ингредиента: {error}")


def add_ingredient_amount(ingredient_id: int, amount: int) -> None:
    """Пополнить запас ингредиента на складе.

    После пополнения автоматически проверяет и обновляет видимость пицц,
    в рецептах которых используется данный ингредиент.

    Args:
        ingredient_id: ID ингредиента
        amount: Количество для добавления

    Raises:
        ValueError: Если amount < 0
        sqlite3.Error: При ошибке работы с БД
    """
    if amount < 0:
        raise ValueError("Количество для добавления не может быть отрицательным")

    try:
        with get_connection() as conn:
            # Проверяем существование ингредиента
            if get_ingredient_by_id(ingredient_id, conn) is None:
                raise ValueError(f"Ингредиент с ID {ingredient_id} не найден")

            # Получаем текущее количество
            current = get_ingredient_amount(ingredient_id, conn)
            new_amount = (current.amount if current else 0) + amount

            # Обновляем количество
            set_ingredient_amount(ingredient_id, new_amount, conn)

            # Обновляем видимость пицц
            update_pizzas_visibility_by_ingredients(conn)

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при пополнении запаса ингредиента: {error}")


def refill_all_ingredients(amount: int) -> None:
    """Пополнить запасы всех ингредиентов на складе.

    Добавляет указанное количество к текущему остатку каждого ингредиента.
    После пополнения автоматически проверяет и обновляет видимость всех пицц.

    Args:
        amount: Количество для добавления к каждому ингредиенту

    Raises:
        ValueError: Если amount < 0
        sqlite3.Error: При ошибке работы с БД
    """
    if amount < 0:
        raise ValueError("Количество для добавления не может быть отрицательным")

    try:
        with get_connection() as conn:
            # Получаем все ингредиенты
            ingredients = get_all_ingredients(conn)

            # Пополняем каждый ингредиент
            for ingredient in ingredients:
                current = get_ingredient_amount(ingredient.id_ingredient, conn)
                new_amount = (current.amount if current else 0) + amount
                set_ingredient_amount(ingredient.id_ingredient, new_amount, conn)

            # Обновляем видимость пицц
            update_pizzas_visibility_by_ingredients(conn)

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при пополнении всех ингредиентов: {error}")


# ======================== Операции с пиццами ========================


def add_pizza(name: str, cost_factor: float = 1.0) -> int:
    """Добавить новую пиццу в меню.

    Создает новую пиццу с указанным названием и множителем стоимости.
    По умолчанию пицца создается видимой для клиентов.

    Args:
        name: Название пиццы
        cost_factor: Множитель стоимости (по умолчанию 1.0)

    Returns:
        ID созданной пиццы

    Raises:
        ValueError: Если cost_factor < 0
        sqlite3.Error: При ошибке работы с БД
    """
    if cost_factor < 0:
        raise ValueError("Множитель стоимости не может быть отрицательным")

    try:
        with get_connection() as conn:
            # Создаем пиццу (по умолчанию видимая)
            pizza_id = create_pizza(name, visible=True, conn=conn)

            # Устанавливаем множитель стоимости
            set_pizza_cost(pizza_id, cost_factor, conn=conn)

            return pizza_id

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при добавлении пиццы: {error}")


def toggle_pizza_visibility(pizza_id: int) -> None:
    """Изменить видимость пиццы в меню.

    Если пицца была видима, становится невидимой и наоборот.

    Args:
        pizza_id: ID пиццы

    Raises:
        ValueError: Если пицца не найдена
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            # Проверяем существование пиццы
            pizza = get_pizza_by_id(pizza_id, conn)
            if pizza is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")

            # Меняем видимость на противоположную
            update_pizza_visibility(pizza_id, not pizza.is_visible, conn)

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при изменении видимости пиццы: {error}")


def delete_pizza(pizza_id: int) -> bool:
    """Удалить пиццу из меню.

    Удаляет пиццу вместе с её рецептом. Операция необратима.

    Args:
        pizza_id: ID пиццы

    Returns:
        True если удаление успешно

    Raises:
        ValueError: Если пицца не найдена
        sqlite3.Error: При ошибке работы с БД
    """

    try:
        with get_connection() as conn:
            # Проверяем существование пиццы
            if get_pizza_by_id(pizza_id, conn) is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")

            # Сначала удаляем рецепт
            delete_recipe_for_pizza(pizza_id, conn)
            # Затем удаляем саму пиццу
            conn.execute(SQL_DELETE_PIZZA, (pizza_id,))  # Прямой SQL вместо рекурсии
            conn.commit()
            return True

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при удалении пиццы: {error}")


# ======================== Операции с рецептами ========================


def add_recipe(pizza_id: int, ingredients: List[Tuple[int, int]]) -> bool:
    """Добавить рецепт для пиццы.

    Создает новый рецепт, связывая пиццу с ингредиентами и их количествами.
    Автоматически проверяет видимость пиццы на основе наличия ингредиентов.

    Args:
        pizza_id: ID пиццы
        ingredients: Список кортежей (id ингредиента, требуемое количество)

    Returns:
        True если рецепт успешно добавлен

    Raises:
        ValueError: Если количество < 0 или ингредиент не существует
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            # Проверяем существование пиццы
            if get_pizza_by_id(pizza_id, conn) is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")

            # Проверяем все ингредиенты
            for ingredient_id, amount in ingredients:
                if amount < 0:
                    raise ValueError(
                        "Количество ингредиента не может быть отрицательным"
                    )
                if get_ingredient_by_id(ingredient_id, conn) is None:
                    raise ValueError(f"Ингредиент с ID {ingredient_id} не найден")

            # Добавляем ингредиенты в рецепт
            for ingredient_id, amount in ingredients:
                upsert_recipe_item(pizza_id, ingredient_id, amount, conn)

            # Проверяем наличие ингредиентов и обновляем видимость
            update_pizzas_visibility_by_ingredients(conn)

            return True

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при добавлении рецепта: {error}")


def update_recipe(pizza_id: int, ingredients: List[Tuple[int, int]]) -> bool:
    """Обновить рецепт пиццы.

    Полностью заменяет существующий рецепт новым.
    Автоматически проверяет видимость пиццы на основе наличия ингредиентов.

    Args:
        pizza_id: ID пиццы
        ingredients: Список кортежей (id ингредиента, требуемое количество)

    Returns:
        True если рецепт успешно обновлен

    Raises:
        ValueError: Если количество < 0 или ингредиент не существует
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            # Проверяем существование пиццы
            if get_pizza_by_id(pizza_id, conn) is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")

            # Проверяем все ингредиенты
            for ingredient_id, amount in ingredients:
                if amount < 0:
                    raise ValueError(
                        "Количество ингредиента не может быть отрицательным"
                    )
                if get_ingredient_by_id(ingredient_id, conn) is None:
                    raise ValueError(f"Ингредиент с ID {ingredient_id} не найден")

            # Удаляем старый рецепт
            delete_recipe_for_pizza(pizza_id, conn)

            # Добавляем новые ингредиенты
            for ingredient_id, amount in ingredients:
                upsert_recipe_item(pizza_id, ingredient_id, amount, conn)

            # Проверяем наличие ингредиентов и обновляем видимость
            update_pizzas_visibility_by_ingredients(conn)

            return True

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при обновлении рецепта: {error}")


def delete_recipe(pizza_id: int) -> bool:
    """Удалить рецепт пиццы.

    Удаляет все записи об ингредиентах для указанной пиццы.
    Автоматически делает пиццу невидимой, так как без рецепта она недоступна.

    Args:
        pizza_id: ID пиццы

    Returns:
        True если удаление успешно

    Raises:
        ValueError: Если пицца не найдена
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:
            # Проверяем существование пиццы
            if get_pizza_by_id(pizza_id, conn) is None:
                raise ValueError(f"Пицца с ID {pizza_id} не найдена")

            # Удаляем рецепт
            delete_recipe_for_pizza(pizza_id, conn)

            # Делаем пиццу невидимой, так как без рецепта она недоступна
            update_pizza_visibility(pizza_id, False, conn)

            return True

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при удалении рецепта: {error}")


# ======================== Служебные функции ========================


# def update_pizzas_visibility_by_ingredients(
#     conn: Optional[sqlite3.Connection] = None,
# ) -> None:
#     """Обновить видимость всех пицц на основе наличия ингредиентов.
#
#     Проверяет наличие всех необходимых ингредиентов для каждой пиццы.
#     Если хотя бы одного ингредиента из рецепта нет на складе (количество = 0),
#     пицца становится невидимой для клиентов.
#
#     Raises:
#         sqlite3.Error: При ошибке работы с БД
#     """
#     try:
#         conn, need_to_close = ensure_connection(conn)
#
#         try:
#             # Получаем все ингредиенты с нулевым количеством
#             all_ingredients = get_all_ingredients(conn)
#             zero_ingredients = set()
#
#             for ingredient in all_ingredients:
#                 amount = get_ingredient_amount(ingredient.id_ingredient, conn)
#                 if amount is None or amount.amount == 0:
#                     zero_ingredients.add(ingredient.id_ingredient)
#
#             if not zero_ingredients:
#                 return
#
#             # Получаем все пиццы
#             all_pizzas = get_all_pizzas(conn)
#
#             # Проверяем каждую пиццу
#             for pizza in all_pizzas:
#                 recipe = get_recipe_for_pizza(pizza.id_pizza, conn)
#                 should_be_visible = True
#
#                 # Если хотя бы один ингредиент с нулевым количеством, скрываем пиццу
#                 for item in recipe:
#                     if item.id_ingredient in zero_ingredients:
#                         should_be_visible = False
#                         break
#
#                 # Обновляем видимость если нужно
#                 if pizza.is_visible != should_be_visible:
#                     update_pizza_visibility(pizza.id_pizza, should_be_visible, conn)
#
#             if need_to_close:
#                 conn.close()
#
#         except sqlite3.Error as error:
#             if need_to_close:
#                 conn.close()
#             raise sqlite3.Error(f"Ошибка при обновлении видимости пицц: {error}")
#
#     except Exception as error:
#         raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


# def get_pizzas_with_ingredient(
#     ingredient_id: int, conn: Optional[sqlite3.Connection] = None
# ) -> Set[int]:
#     """Найти все пиццы, в рецептах которых используется указанный ингредиент.
#
#     Args:
#         ingredient_id: ID ингредиента
#         conn: Соединение с базой данных. Если None или невалидное - создается новое.
#
#     Returns:
#         Множество ID пицц, использующих данный ингредиент
#
#     Raises:
#         sqlite3.Error: При ошибке работы с БД
#     """
#     try:
#         conn, need_to_close = ensure_connection(conn)
#
#         try:
#             # Получаем все рецепты
#             all_recipes = get_all_recipes(None, conn)  # Используем новую функцию
#
#             # Собираем ID пицц, использующих данный ингредиент
#             pizza_ids = {
#                 recipe.id_pizza
#                 for recipe in all_recipes
#                 if recipe.id_ingredient == ingredient_id
#             }
#
#             if need_to_close:
#                 conn.close()
#
#             return pizza_ids
#
#         except sqlite3.Error as error:
#             if need_to_close:
#                 conn.close()
#             raise sqlite3.Error(f"Ошибка при поиске пицц с ингредиентом: {error}")
#
#     except Exception as error:
#         raise sqlite3.Error(f"Ошибка при работе с БД: {error}")


def get_pizzas_with_ingredient(ingredient_id: int) -> Set[int]:  # Убираем параметр conn
    """Найти все пиццы, в рецептах которых используется указанный ингредиент.

    Args:
        ingredient_id: ID ингредиента

    Returns:
        Множество ID пицц, использующих данный ингредиент

    Raises:
        sqlite3.Error: При ошибке работы с БД
    """
    try:
        with get_connection() as conn:  # Используем with вместо ensure_connection
            # Получаем все рецепты
            all_recipes = get_all_recipes(conn)  # Передаем только conn

            # Собираем ID пицц, использующих данный ингредиент
            pizza_ids = {
                recipe.id_pizza
                for recipe in all_recipes
                if recipe.id_ingredient == ingredient_id
            }

            return pizza_ids

    except sqlite3.Error as error:
        raise sqlite3.Error(f"Ошибка при поиске пицц с ингредиентом: {error}")
