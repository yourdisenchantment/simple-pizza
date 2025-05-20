# app/ui/admin_menu.py

from app.admin.operations import *


def show_admin_menu() -> None:
    """Показать меню администратора."""
    while True:
        print("\n=== Меню администратора ===")
        print("\nРабота с ингредиентами:")
        print("1. Добавить ингредиент")
        print("2. Удалить ингредиент")
        print("3. Изменить стоимость ингредиента")
        print("4. Пополнить количество ингредиента")
        print("5. Пополнить все ингредиенты")

        print("\nРабота с пиццами:")
        print("6. Добавить пиццу")
        print("7. Изменить видимость пиццы")
        print("8. Удалить пиццу")

        print("\nРабота с рецептами:")
        print("9. Добавить рецепт")
        print("10. Изменить рецепт")
        print("11. Удалить рецепт")

        print("\n0. Вернуться в главное меню")

        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                add_new_ingredient()
            case "2":
                remove_ingredient()
            case "3":
                change_ingredient_cost()
            case "4":
                refill_ingredient()
            case "5":
                refill_all()
            case "6":
                add_new_pizza()
            case "7":
                toggle_pizza()
            case "8":
                remove_pizza()
            case "9":
                add_new_recipe()
            case "10":
                modify_recipe()
            case "11":
                remove_recipe()
            case "0":
                break
            case _:
                print("Неверный выбор. Попробуйте снова.")


# ======================== Операции с ингредиентами ========================


def show_all_ingredients() -> None:
    """Показать список всех ингредиентов."""
    try:
        ingredients = get_all_ingredients()
        if not ingredients:
            print("\nСписок ингредиентов пуст")
            return

        print("\nСписок ингредиентов:")
        for ingredient in ingredients:
            amount = get_ingredient_amount(ingredient.id_ingredient)
            cost = get_ingredient_cost(ingredient.id_ingredient)
            print(
                f"{ingredient.id_ingredient}. {ingredient.name_ingredient} "
                f"(остаток: {amount.amount if amount else 0}, "
                f"цена: {cost.cost if cost else 0:.2f})"
            )

    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def add_new_ingredient() -> None:
    """Добавить новый ингредиент."""
    try:
        print("\n=== Добавление ингредиента ===")

        name = input("Введите название ингредиента: ")
        if not name.strip():
            print("Название не может быть пустым")
            return

        cost = float(input("Введите стоимость за единицу: "))
        amount = int(input("Введите начальное количество: "))

        ingredient_id = add_ingredient(name, cost, amount)
        print(f"\nИнгредиент успешно добавлен (ID: {ingredient_id})")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def remove_ingredient() -> None:
    """Удалить ингредиент."""
    try:
        print("\n=== Удаление ингредиента ===")
        show_all_ingredients()

        ingredient_id = int(input("\nВведите ID ингредиента: "))
        force = (
            input("Удалить вместе со всеми зависимыми пиццами? (y/n): ").lower() == "y"
        )

        if delete_ingredient(ingredient_id, force):
            print("\nИнгредиент успешно удален")
        else:
            print("\nНевозможно удалить ингредиент (используется в рецептах)")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def change_ingredient_cost() -> None:
    """Изменить стоимость ингредиента."""
    try:
        print("\n=== Изменение стоимости ингредиента ===")
        show_all_ingredients()

        ingredient_id = int(input("\nВведите ID ингредиента: "))
        new_cost = float(input("Введите новую стоимость: "))

        update_ingredient_cost(ingredient_id, new_cost)
        print("\nСтоимость успешно обновлена")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def refill_ingredient() -> None:
    """Пополнить запас ингредиента."""
    try:
        print("\n=== Пополнение запаса ингредиента ===")
        show_all_ingredients()

        ingredient_id = int(input("\nВведите ID ингредиента: "))
        amount = int(input("Введите количество для добавления: "))

        add_ingredient_amount(ingredient_id, amount)
        print("\nЗапас успешно пополнен")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def refill_all() -> None:
    """Пополнить запас всех ингредиентов."""
    try:
        print("\n=== Пополнение всех ингредиентов ===")
        show_all_ingredients()

        amount = int(
            input("\nВведите количество для добавления ко всем ингредиентам: ")
        )

        refill_all_ingredients(amount)
        print("\nЗапасы всех ингредиентов успешно пополнены")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


# ======================== Операции с пиццами ========================


def show_all_pizzas() -> None:
    """Показать список всех пицц."""
    try:
        pizzas = get_all_pizzas()
        if not pizzas:
            print("\nСписок пицц пуст")
            return

        print("\nСписок пицц:")
        for pizza in pizzas:
            cost = get_pizza_cost(pizza.id_pizza)
            status = "видима" if pizza.is_visible else "скрыта"
            print(
                f"{pizza.id_pizza}. {pizza.name_pizza} "
                f"(стоимость: {cost:.2f if cost else 'не задана'}, "
                f"статус: {status})"
            )

    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def show_pizza_recipe(pizza_id: int) -> None:
    """Показать рецепт конкретной пиццы."""
    try:
        recipe = get_recipe_for_pizza(pizza_id)
        if not recipe:
            print("\nРецепт не найден")
            return

        print("\nСостав:")
        for item in recipe:
            ingredient = get_ingredient_by_id(item.id_ingredient)
            if ingredient:
                print(f"- {ingredient.name_ingredient}: {item.amount} шт.")

    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def add_new_pizza() -> None:
    """Добавить новую пиццу."""
    try:
        print("\n=== Добавление новой пиццы ===")

        name = input("Введите название пиццы: ")
        if not name.strip():
            print("Название не может быть пустым")
            return

        cost_factor = float(
            input("Введите множитель стоимости (1.0 по умолчанию): ") or 1.0
        )

        pizza_id = add_pizza(name, cost_factor)
        print(f"\nПицца успешно добавлена (ID: {pizza_id})")
        print("Не забудьте добавить рецепт для новой пиццы!")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def toggle_pizza() -> None:
    """Изменить видимость пиццы."""
    try:
        print("\n=== Изменение видимости пиццы ===")
        show_all_pizzas()

        pizza_id = int(input("\nВведите ID пиццы: "))

        toggle_pizza_visibility(pizza_id)
        print("\nВидимость пиццы успешно изменена")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def remove_pizza() -> None:
    """Удалить пиццу."""
    try:
        print("\n=== Удаление пиццы ===")
        show_all_pizzas()

        pizza_id = int(input("\nВведите ID пиццы: "))

        confirm = input("Вы уверены? Это действие нельзя отменить (y/n): ").lower()
        if confirm != "y":
            print("\nУдаление отменено")
            return

        if delete_pizza(pizza_id):
            print("\nПицца успешно удалена")
        else:
            print("\nНе удалось удалить пиццу")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


# ======================== Операции с рецептами ========================


# noinspection DuplicatedCode
def add_new_recipe() -> None:
    """Добавить новый рецепт."""
    try:
        print("\n=== Добавление рецепта ===")
        show_all_pizzas()
        pizza_id = int(input("\nВведите ID пиццы: "))

        # noinspection DuplicatedCode
        print("\nДоступные ингредиенты:")
        show_all_ingredients()

        ingredients = []
        while True:
            try:
                ingredient_id = int(
                    input("\nВведите ID ингредиента (0 для завершения): ")
                )
                if ingredient_id == 0:
                    break

                amount = int(input("Введите количество: "))
                ingredients.append((ingredient_id, amount))

            except ValueError:
                print("Некорректный ввод, попробуйте снова")

        if not ingredients:
            print("Рецепт не может быть пустым")
            return

        if add_recipe(pizza_id, ingredients):
            print("\nРецепт успешно добавлен")
        else:
            print("\nНе удалось добавить рецепт")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


# noinspection DuplicatedCode
def modify_recipe() -> None:
    """Изменить существующий рецепт."""
    try:
        print("\n=== Изменение рецепта ===")
        show_all_pizzas()
        pizza_id = int(input("\nВведите ID пиццы: "))

        print("\nТекущий рецепт:")
        show_pizza_recipe(pizza_id)

        # noinspection DuplicatedCode
        print("\nДоступные ингредиенты:")
        show_all_ingredients()

        ingredients = []
        while True:
            try:
                ingredient_id = int(
                    input("\nВведите ID ингредиента (0 для завершения): ")
                )
                if ingredient_id == 0:
                    break

                amount = int(input("Введите количество: "))
                ingredients.append((ingredient_id, amount))

            except ValueError:
                print("Некорректный ввод, попробуйте снова")

        if not ingredients:
            print("Рецепт не может быть пустым")
            return

        if update_recipe(pizza_id, ingredients):
            print("\nРецепт успешно обновлен")
        else:
            print("\nНе удалось обновить рецепт")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def remove_recipe() -> None:
    """Удалить рецепт."""
    try:
        print("\n=== Удаление рецепта ===")
        show_all_pizzas()
        pizza_id = int(input("\nВведите ID пиццы: "))

        print("\nТекущий рецепт:")
        show_pizza_recipe(pizza_id)

        confirm = input("\nВы уверены? Пицца станет недоступной (y/n): ").lower()
        if confirm != "y":
            print("\nУдаление отменено")
            return

        if delete_recipe(pizza_id):
            print("\nРецепт успешно удален")
        else:
            print("\nНе удалось удалить рецепт")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")
