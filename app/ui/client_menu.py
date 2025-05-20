# app/ui/client_menu.py

from app.client.operations import *


def show_client_menu() -> None:
    """Показать меню клиента."""
    while True:
        print("\n=== Меню клиента ===")
        print("1. Посмотреть доступные пиццы")
        print("2. Посмотреть детали пиццы")
        print("3. Заказать пиццу")
        print("0. Вернуться в главное меню")

        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                show_available_pizzas()
            case "2":
                show_pizza_details()
            case "3":
                make_order()
            case "0":
                break
            case _:
                print("Неверный выбор. Попробуйте снова.")


def show_available_pizzas() -> None:
    """Показать список доступных пицц."""
    try:
        pizzas = get_available_pizzas()
        if not pizzas:
            print("\nНет доступных пицц")
            return

        print("\nДоступные пиццы:")
        for pizza, price in pizzas:
            print(f"{pizza.id_pizza}. {pizza.name_pizza} - {price:.2f} руб.")

    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def show_pizza_details() -> None:
    """Показать детали конкретной пиццы."""
    try:
        pizza_id = int(input("\nВведите номер пиццы: "))
        pizza, ingredients, price = get_pizza_details(pizza_id)

        print(f"\nПицца '{pizza.name_pizza}'")
        print("\nСостав:")
        for ingredient, amount in ingredients:
            print(f"- {ingredient.name_ingredient}: {amount} шт.")
        print(f"\nЦена: {price:.2f} руб.")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")


def make_order() -> None:
    """Оформить заказ пиццы."""
    try:
        pizza_id = int(input("\nВведите номер пиццы: "))

        if order_pizza(pizza_id):
            print("\nЗаказ успешно оформлен!")
        else:
            print("\nНе удалось оформить заказ")

    except ValueError as error:
        print(f"\nОшибка: {error}")
    except sqlite3.Error as error:
        print(f"\nОшибка: {error}")
