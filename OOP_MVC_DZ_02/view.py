class MenuView:
    """Класс для отображения меню и навигации."""

    @staticmethod
    def show_main_menu():
        """Отображает главное меню программы."""
        print("\n" + "="*50)
        print("ТЕЛЕФОННЫЙ СПРАВОЧНИК".center(50))
        print("="*50)
        print("1. Показать все контакты")
        print("2. Создать контакт")
        print("3. Найти контакт")
        print("4. Изменить контакт")
        print("5. Удалить контакт")
        print("6. Выход")
        print("="*50)

    @staticmethod
    def get_user_choice() -> str:
        """Получает выбор пользователя из меню."""
        return input("Выберите действие (1-6): ").strip()


class ContactView:
    """Класс для отображения и ввода данных контактов."""

    @staticmethod
    def show_contacts(contacts: list) -> None:
        """
        Отображает список контактов.

        Args:
            contacts: Список строк с контактами
        """
        if not contacts:
            print("\nСправочник пуст.")
            return

        print("\n" + "-"*50)
        print("СПИСОК КОНТАКТОВ".center(50))
        print("-"*50)

        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact.strip()}")

        print("-"*50)
        print(f"Всего контактов: {len(contacts)}")

    @staticmethod
    def show_contact_detail(contact_data: str) -> None:
        """
        Отображает детальную информацию о контакте.

        Args:
            contact_data: Строка с данными контакта
        """
        if contact_data:
            print("\n" + "-"*50)
            print("ИНФОРМАЦИЯ О КОНТАКТЕ".center(50))
            print("-"*50)
            print(contact_data)
            print("-"*50)
        else:
            print("\nКонтакт не найден.")

    @staticmethod
    def get_new_contact_data() -> tuple:
        """
        Запрашивает у пользователя данные для нового контакта.

        Returns:
            Кортеж (имя, телефон, комментарий)
        """
        print("\n--- СОЗДАНИЕ НОВОГО КОНТАКТА ---")
        name = input("Введите имя: ").strip()

        # Проверка на пустое имя
        while not name:
            print("Ошибка: Имя не может быть пустым!")
            name = input("Введите имя: ").strip()

        number = input("Введите номер телефона: ").strip()

        # Проверка на пустой номер
        while not number:
            print("Ошибка: Номер телефона не может быть пустым!")
            number = input("Введите номер телефона: ").strip()

        note = input("Введите комментарий (необязательно): ").strip()

        return name, number, note

    @staticmethod
    def get_search_query() -> str:
        """Запрашивает поисковый запрос."""
        return input("\nВведите имя контакта для поиска: ").strip()

    @staticmethod
    def get_contact_name_for_action(action: str) -> str:
        """
        Запрашивает имя контакта для выполнения действия.
        """
        return input(f"\nВведите имя контакта для {action}: ").strip()

    @staticmethod
    def get_updated_contact_data() -> tuple:
        """
        Запрашивает обновленные данные контакта.

        Returns:
            Кортеж (новое имя, новый телефон, новый комментарий)
        """
        print("\n--- ВВЕДИТЕ НОВЫЕ ДАННЫЕ ---")
        new_name = input("Новое имя: ").strip()
        new_number = input("Новый номер: ").strip()
        new_note = input("Новый комментарий: ").strip()

        return new_name, new_number, new_note

    @staticmethod
    def exit_programm():
        """Красивое завершение программы."""
        print("\n" + "="*50)
        print("✨ Спасибо за использование программы! До свидания! ✨")
        print("="*50 + "\n")
