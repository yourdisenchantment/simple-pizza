# app/ui/main_menu.py


def show_main_menu() -> None:
    """Показать главное меню приложения."""
    while True:
        print("\n=== Пиццерия ===")
        print("1. Войти как клиент")
        print("2. Войти как администратор")
        print("0. Выход")

        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                from app.ui.client_menu import show_client_menu

                show_client_menu()
            case "2":
                from app.ui.admin_menu import show_admin_menu

                show_admin_menu()
            case "0":
                print("До свидания!")
                break
            case _:
                print("Неверный выбор. Попробуйте снова.")
