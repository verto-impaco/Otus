from model import PhoneBook, FileRead, PATH
from view import MenuView, ContactView


class CustomExceptions:
    """Класс с кастомными исключениями."""

    class ContactNotFoundError(Exception):
        """Исключение при ненайденном контакте."""
        pass

    class InvalidInputError(Exception):
        """Исключение при некорректном вводе."""
        pass

    class EmptyPhoneBookError(Exception):
        """Исключение при пустом справочнике."""
        pass


class PhoneBookController:
    """
    Контроллер телефонного справочника.
    Координирует работу модели и представления.
    """

    def __init__(self):
        """Инициализация контроллера."""
        self.phone_book = PhoneBook()
        self.menu_view = MenuView()
        self.contact_view = ContactView()
        self.current_file = PATH
        self.changes_made = False

    def run(self):
        """Запускает основной цикл программы."""
        stop_programm = True
        while stop_programm:

            self.menu_view.show_main_menu()
            choice = self.menu_view.get_user_choice()

            if choice == '1':
                self._show_all_contacts()
            elif choice == '2':
                self._create_contact()
            elif choice == '3':
                self._find_contact()
            elif choice == '4':
                self._change_contact()
            elif choice == '5':
                self._delete_contact()
            elif choice == '6':
                self._exit_program()
                stop_programm = False
            else:
                print(
                    "Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")

    def _show_all_contacts(self):
        """Показывает все контакты."""

        contacts = FileRead.file_read(self.current_file)
        if contacts:
            self.contact_view.show_contacts(contacts)
        else:
            raise CustomExceptions.EmptyPhoneBookError(
                "Не удалось прочитать контакты")

    def _create_contact(self):
        """Создает новый контакт."""
        name, number, note = self.contact_view.get_new_contact_data()

        # Дополнительная валидация
        if not name or not number:
            raise CustomExceptions.InvalidInputError(
                "Имя и номер телефона обязательны для заполнения")

        self.phone_book.create_contact(name, number, note)

    def _find_contact(self):
        """Ищет контакт по имени."""
        search_name = self.contact_view.get_search_query()

        contact = self.phone_book.find_contact(search_name)

        if contact:
            self.contact_view.show_contact_detail(contact)
        else:
            print(f"Контакт '{search_name}' не найден")

    def _change_contact(self):
        """Изменяет существующий контакт."""
        contact_name = self.contact_view.get_contact_name_for_action(
            "изменения")

        # Проверяем существование контакта
        existing_contact = self.phone_book.find_contact(contact_name)
        if not existing_contact:
            raise CustomExceptions.ContactNotFoundError(
                print(f"Контакт '{contact_name}' не найден"))

        # Показываем текущие данные
        self.contact_view.show_contact_detail(existing_contact)

        new_name, new_number, new_note = self.contact_view.get_updated_contact_data()

        if not new_name and not new_number and not new_note:
            raise CustomExceptions.InvalidInputError(print(
                "Не введены новые данные для изменения"))

        old_parts = existing_contact.split('=')
        if len(old_parts) > 1:
            old_data = old_parts[1].strip().split()
            old_number = old_data[0] if old_data else ''
            old_note = ' '.join(old_data[1:]) if len(old_data) > 1 else ''

            new_name = new_name or contact_name
            new_number = new_number or old_number
            new_note = new_note or old_note

        self.phone_book.change_contact(
            contact_name, new_name, new_number, new_note)
        self.changes_made = True

    def _delete_contact(self):
        """Удаляет контакт."""
        contact_name = self.contact_view.get_contact_name_for_action(
            "удаления")

        if not contact_name:
            raise CustomExceptions.InvalidInputError(
                "Имя контакта не может быть пустым")

        existing_contact = self.phone_book.find_contact(contact_name)
        if not existing_contact:
            raise CustomExceptions.ContactNotFoundError(
                print(f"Контакт '{contact_name}' не найден"))

        self.phone_book.delete_contact(contact_name)

    def _exit_program(self):
        """Завершает работу программы с проверкой несохраненных изменений."""
        self.contact_view.exit_programm()
