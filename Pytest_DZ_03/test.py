from model import Contact, FileWrite, FileRead, PhoneBook, PATH
from controller import PhoneBookController, CustomExceptions
from view import MenuView, ContactView
import sys
import os
import pytest
from unittest.mock import Mock, patch, mock_open, MagicMock
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


# Фикстуры
@pytest.fixture
def temp_file_path(tmp_path):
    """Создает временный файл для тестов."""
    file_path = tmp_path / "test_phonebook.txt"
    return str(file_path)


@pytest.fixture
def phonebook_with_data(temp_file_path):
    """Создает телефонную книгу с тестовыми данными."""
    pb = PhoneBook(temp_file_path)
    pb.create_contact("Иван Петров", "123-456", "друг")
    pb.create_contact("Мария Иванова", "789-012", "коллега")
    return pb


# Тесты для модели (model.py)
class TestContact:
    """Тесты для dataclass Contact."""

    def test_contact_creation(self):
        """Тест создания контакта."""
        contact = Contact("Тест", "123", "заметка")
        assert contact.name == "Тест"
        assert contact.number == "123"
        assert contact.note == "заметка"

    def test_contact_default_note(self):
        """Тест создания контакта с заметкой по умолчанию."""
        contact = Contact("Тест", "123")
        assert contact.note == ""


class TestFileWrite:
    """Тесты для класса FileWrite."""

    @patch("builtins.open", new_callable=mock_open)
    def test_file_write_success(self, mock_file):
        """Тест успешной записи в файл."""
        FileWrite.file_write("test.txt", ["line1\n", "line2\n"])
        mock_file.assert_called_once_with("test.txt", "w", encoding="utf-8")
        mock_file().writelines.assert_called_once_with(["line1\n", "line2\n"])

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_file_write_file_not_found(self, mock_print, mock_open):
        """Тест обработки FileNotFoundError при записи."""
        FileWrite.file_write("nonexistent.txt", ["data"])
        mock_print.assert_called_once_with("Файл не найден.")

    @patch("builtins.open", new_callable=mock_open)
    def test_file_append_success(self, mock_file):
        """Тест успешного добавления в файл."""
        FileWrite.file_append("test.txt", "new line\n")
        mock_file.assert_called_once_with("test.txt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("new line\n")

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_file_append_file_not_found(self, mock_print, mock_open):
        """Тест обработки FileNotFoundError при добавлении."""
        FileWrite.file_append("nonexistent.txt", "data")
        mock_print.assert_called_once_with("Файл не найден.")


class TestFileRead:
    """Тесты для класса FileRead."""

    @patch("builtins.open", new_callable=mock_open, read_data="line1\nline2\n")
    def test_file_read_success(self, mock_file):
        """Тест успешного чтения файла."""
        result = FileRead.file_read("test.txt")
        assert result == ["line1\n", "line2\n"]
        mock_file.assert_called_once_with("test.txt", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_file_read_empty_file(self, mock_file):
        """Тест чтения пустого файла."""
        result = FileRead.file_read("empty.txt")
        assert result == []


class TestPhoneBook:
    """Тесты для класса PhoneBook."""

    def test_init_default_path(self):
        """Тест инициализации с путем по умолчанию."""
        pb = PhoneBook()
        assert pb.path == PATH

    def test_init_custom_path(self, temp_file_path):
        """Тест инициализации с пользовательским путем."""
        pb = PhoneBook(temp_file_path)
        assert pb.path == temp_file_path

    @patch.object(FileWrite, "file_append")
    def test_create_contact(self, mock_append, temp_file_path):
        """Тест создания контакта."""
        pb = PhoneBook(temp_file_path)
        pb.create_contact("Иван", "123", "заметка")

        # Проверяем, что метод file_append был вызван
        assert mock_append.called
        # Проверяем аргументы
        args, kwargs = mock_append.call_args
        assert args[0] == temp_file_path
        assert "Иван = " in args[1]
        assert "123" in args[1]
        assert "заметка" in args[1]

    def test_create_and_find_contact(self, phonebook_with_data, temp_file_path):
        """Тест создания и поиска контакта."""
        pb = phonebook_with_data
        contact = pb.find_contact("Иван Петров")
        assert contact is not None
        assert "Иван Петров =" in contact
        assert "123-456" in contact

    def test_find_nonexistent_contact(self, phonebook_with_data):
        """Тест поиска несуществующего контакта."""
        pb = phonebook_with_data
        contact = pb.find_contact("Несуществующий")
        assert contact is None

    @patch.object(FileRead, "file_read")
    def test_find_contact_none_lines(self, mock_read, temp_file_path):
        """Тест поиска контакта при ошибке чтения файла."""
        mock_read.return_value = None
        pb = PhoneBook(temp_file_path)
        result = pb.find_contact("Иван")
        assert result is None

    @patch.object(FileWrite, "file_write")
    def test_change_contact_success(self, mock_write, phonebook_with_data, temp_file_path):
        """Тест успешного изменения контакта."""
        pb = phonebook_with_data
        with patch("builtins.print") as mock_print:
            pb.change_contact("Иван Петров", "Петр Иванов",
                              "999-999", "новый друг")

        # Проверяем, что file_write был вызван
        assert mock_write.called
        # Проверяем аргументы
        args, kwargs = mock_write.call_args
        assert args[0] == temp_file_path
        # Проверяем, что контакт был изменен
        lines = args[1]
        assert any("Петр Иванов = 999-999 новый друг" in line for line in lines)
        # Проверяем, что старый контакт отсутствует
        assert not any("Иван Петров" in line for line in lines)

    @patch.object(FileWrite, "file_write")
    def test_change_nonexistent_contact(self, mock_write, phonebook_with_data):
        """Тест изменения несуществующего контакта."""
        pb = phonebook_with_data
        with patch("builtins.print") as mock_print:
            pb.change_contact("Несущ", "Новый", "111", "прим")

        assert not mock_write.called
        mock_print.assert_called_with('Контакт не найден в справочнике.')

    @patch.object(FileRead, "file_read")
    def test_change_contact_read_error(self, mock_read, temp_file_path):
        """Тест изменения при ошибке чтения файла."""
        mock_read.return_value = None
        pb = PhoneBook(temp_file_path)
        with patch("builtins.print") as mock_print:
            pb.change_contact("Иван", "Петр", "123", "note")

        mock_print.assert_called_with("Файл не найден или пуст")

    def test_delete_contact(self, phonebook_with_data, temp_file_path):
        """Тест удаления контакта."""
        pb = phonebook_with_data
        result = pb.delete_contact("Иван Петров")

        # Проверяем, что контакт удален
        contact = pb.find_contact("Иван Петров")
        assert contact is None

        # Проверяем, что второй контакт остался
        contact2 = pb.find_contact("Мария Иванова")
        assert contact2 is not None

    @patch.object(FileRead, "file_read")
    def test_delete_contact_read_error(self, mock_read, temp_file_path):
        """Тест удаления при ошибке чтения файла."""
        mock_read.return_value = None
        pb = PhoneBook(temp_file_path)
        with patch("builtins.print") as mock_print:
            result = pb.delete_contact("Иван")

        mock_print.assert_called_with(
            f"Не удалось прочитать файл {temp_file_path}")

    @patch("os.path.getsize")
    @patch.object(FileRead, "file_read")
    def test_show_all_contacts_empty(self, mock_read, mock_getsize, phonebook_with_data):
        """Тест показа контактов при пустом файле."""
        mock_getsize.return_value = 0
        with patch("builtins.print") as mock_print:
            phonebook_with_data.show_all_contacts()

        mock_print.assert_called_with('В справочнике отсутствуют контакты')

    @patch("os.path.getsize")
    @patch.object(FileRead, "file_read")
    def test_show_all_contacts_with_data(self, mock_read, mock_getsize, phonebook_with_data):
        """Тест показа контактов с данными."""
        mock_getsize.return_value = 100
        mock_read.return_value = ["Иван Петров = 123-456 друг\n"]
        with patch("builtins.print") as mock_print:
            phonebook_with_data.show_all_contacts()

        mock_print.assert_called_with(["Иван Петров = 123-456 друг\n"])


# Тесты для контроллера (controller.py)
class TestCustomExceptions:
    """Тесты для кастомных исключений."""

    def test_contact_not_found_error(self):
        """Тест исключения ContactNotFoundError."""
        with pytest.raises(CustomExceptions.ContactNotFoundError):
            raise CustomExceptions.ContactNotFoundError("Контакт не найден")

    def test_invalid_input_error(self):
        """Тест исключения InvalidInputError."""
        with pytest.raises(CustomExceptions.InvalidInputError):
            raise CustomExceptions.InvalidInputError("Неверный ввод")

    def test_empty_phone_book_error(self):
        """Тест исключения EmptyPhoneBookError."""
        with pytest.raises(CustomExceptions.EmptyPhoneBookError):
            raise CustomExceptions.EmptyPhoneBookError("Справочник пуст")


class TestPhoneBookController:
    """Тесты для PhoneBookController."""

    @patch("controller.PATH", "test_path.txt")
    def test_init(self):
        """Тест инициализации контроллера."""
        controller = PhoneBookController()
        assert controller.current_file == "test_path.txt"
        assert controller.changes_made is False
        assert controller.phone_book is not None
        assert controller.menu_view is not None
        assert controller.contact_view is not None

    @patch.object(MenuView, "show_main_menu")
    @patch.object(MenuView, "get_user_choice")
    @patch.object(PhoneBookController, "_exit_program")
    def test_run_exit(self, mock_exit, mock_get_choice, mock_show_menu):
        """Тест запуска программы с выходом."""
        mock_get_choice.return_value = "6"
        controller = PhoneBookController()

        with patch("builtins.print"):  # Подавляем вывод
            controller.run()

        mock_show_menu.assert_called_once()
        mock_get_choice.assert_called_once()
        mock_exit.assert_called_once()

    @patch.object(MenuView, "get_user_choice")
    def test_run_invalid_choice(self, mock_get_choice):
        """Тест обработки неверного выбора."""
        mock_get_choice.side_effect = [
            "invalid", "6"]  # Сначала неверный, потом выход
        controller = PhoneBookController()

        with patch("builtins.print") as mock_print:
            controller.run()

        # Проверяем, что сообщение об ошибке было выведено
        error_calls = [call for call in mock_print.call_args_list
                       if "Неверный выбор" in str(call)]
        assert len(error_calls) > 0

    @patch.object(PhoneBookController, "_show_all_contacts")
    @patch.object(MenuView, "get_user_choice")
    def test_run_show_all(self, mock_get_choice, mock_show_all):
        """Тест выбора пункта 'Показать все контакты'."""
        mock_get_choice.side_effect = ["1", "6"]
        controller = PhoneBookController()

        with patch("builtins.print"):
            controller.run()

        mock_show_all.assert_called_once()

    @patch.object(FileRead, "file_read")
    @patch.object(ContactView, "show_contacts")
    def test_show_all_contacts_success(self, mock_show, mock_read):
        """Тест успешного показа всех контактов."""
        mock_read.return_value = ["contact1\n", "contact2\n"]
        controller = PhoneBookController()

        controller._show_all_contacts()

        mock_show.assert_called_once_with(["contact1\n", "contact2\n"])

    @patch.object(FileRead, "file_read")
    def test_show_all_contacts_empty(self, mock_read):
        """Тест показа пустого справочника."""
        mock_read.return_value = []
        controller = PhoneBookController()

        with pytest.raises(CustomExceptions.EmptyPhoneBookError):
            controller._show_all_contacts()

    @patch.object(ContactView, "get_new_contact_data")
    @patch.object(PhoneBook, "create_contact")
    def test_create_contact_success(self, mock_create, mock_get_data):
        """Тест успешного создания контакта."""
        mock_get_data.return_value = ("Иван", "123", "заметка")
        controller = PhoneBookController()

        controller._create_contact()

        mock_create.assert_called_once_with("Иван", "123", "заметка")

    @patch.object(ContactView, "get_new_contact_data")
    def test_create_contact_invalid_input(self, mock_get_data):
        """Тест создания контакта с неверными данными."""
        mock_get_data.return_value = ("", "123", "")  # Пустое имя
        controller = PhoneBookController()

        with pytest.raises(CustomExceptions.InvalidInputError):
            controller._create_contact()

        mock_get_data.return_value = ("Иван", "", "")  # Пустой номер
        with pytest.raises(CustomExceptions.InvalidInputError):
            controller._create_contact()

    @patch.object(ContactView, "get_search_query")
    @patch.object(PhoneBook, "find_contact")
    @patch.object(ContactView, "show_contact_detail")
    def test_find_contact_found(self, mock_show, mock_find, mock_query):
        """Тест поиска существующего контакта."""
        mock_query.return_value = "Иван"
        mock_find.return_value = "Иван = 123"
        controller = PhoneBookController()

        with patch("builtins.print"):
            controller._find_contact()

        mock_show.assert_called_once_with("Иван = 123")

    @patch.object(ContactView, "get_search_query")
    @patch.object(PhoneBook, "find_contact")
    def test_find_contact_not_found(self, mock_find, mock_query):
        """Тест поиска несуществующего контакта."""
        mock_query.return_value = "Иван"
        mock_find.return_value = None
        controller = PhoneBookController()

        with patch("builtins.print") as mock_print:
            controller._find_contact()

        mock_print.assert_called_with("Контакт 'Иван' не найден")

    @patch.object(ContactView, "get_contact_name_for_action")
    @patch.object(PhoneBook, "find_contact")
    @patch.object(ContactView, "get_updated_contact_data")
    @patch.object(PhoneBook, "change_contact")
    @patch.object(ContactView, "show_contact_detail")
    def test_change_contact_success(self, mock_show, mock_change, mock_get_data,
                                    mock_find, mock_get_name):
        """Тест успешного изменения контакта."""
        mock_get_name.return_value = "Иван"
        mock_find.return_value = "Иван = 123 старая_заметка"
        mock_get_data.return_value = ("Петр", "456", "новая_заметка")
        controller = PhoneBookController()

        with patch("builtins.print"):
            controller._change_contact()

        mock_change.assert_called_once()
        assert controller.changes_made is True

    @patch.object(ContactView, "get_contact_name_for_action")
    @patch.object(PhoneBook, "find_contact")
    def test_change_contact_not_found(self, mock_find, mock_get_name):
        """Тест изменения несуществующего контакта."""
        mock_get_name.return_value = "Иван"
        mock_find.return_value = None
        controller = PhoneBookController()

        with pytest.raises(CustomExceptions.ContactNotFoundError):
            controller._change_contact()

    @patch.object(ContactView, "get_contact_name_for_action")
    @patch.object(PhoneBook, "find_contact")
    @patch.object(ContactView, "get_updated_contact_data")
    def test_change_contact_no_new_data(self, mock_get_data, mock_find, mock_get_name):
        """Тест изменения без новых данных."""
        mock_get_name.return_value = "Иван"
        mock_find.return_value = "Иван = 123"
        mock_get_data.return_value = ("", "", "")
        controller = PhoneBookController()

        with pytest.raises(CustomExceptions.InvalidInputError):
            controller._change_contact()

    @patch.object(ContactView, "get_contact_name_for_action")
    @patch.object(PhoneBook, "find_contact")
    @patch.object(PhoneBook, "delete_contact")
    def test_delete_contact_success(self, mock_delete, mock_find, mock_get_name):
        """Тест успешного удаления контакта."""
        mock_get_name.return_value = "Иван"
        mock_find.return_value = "Иван = 123"
        controller = PhoneBookController()

        controller._delete_contact()

        mock_delete.assert_called_once_with("Иван")

    @patch.object(ContactView, "get_contact_name_for_action")
    def test_delete_contact_empty_name(self, mock_get_name):
        """Тест удаления с пустым именем."""
        mock_get_name.return_value = ""
        controller = PhoneBookController()

        with pytest.raises(CustomExceptions.InvalidInputError):
            controller._delete_contact()

    @patch.object(ContactView, "get_contact_name_for_action")
    @patch.object(PhoneBook, "find_contact")
    def test_delete_contact_not_found(self, mock_find, mock_get_name):
        """Тест удаления несуществующего контакта."""
        mock_get_name.return_value = "Иван"
        mock_find.return_value = None
        controller = PhoneBookController()

        with pytest.raises(CustomExceptions.ContactNotFoundError):
            controller._delete_contact()

    @patch.object(ContactView, "exit_programm")
    def test_exit_program(self, mock_exit):
        """Тест выхода из программы."""
        controller = PhoneBookController()
        controller._exit_program()
        mock_exit.assert_called_once()


# Тесты для представления (view.py)
class TestMenuView:
    """Тесты для MenuView."""

    def test_show_main_menu(self, capsys):
        """Тест отображения главного меню."""
        MenuView.show_main_menu()
        captured = capsys.readouterr()
        assert "ТЕЛЕФОННЫЙ СПРАВОЧНИК" in captured.out
        assert "1. Показать все контакты" in captured.out
        assert "6. Выход" in captured.out

    @patch("builtins.input", return_value="3")
    def test_get_user_choice(self, mock_input):
        """Тест получения выбора пользователя."""
        result = MenuView.get_user_choice()
        assert result == "3"
        mock_input.assert_called_once_with("Выберите действие (1-6): ")


class TestContactView:
    """Тесты для ContactView."""

    def test_show_contacts_with_data(self, capsys):
        """Тест отображения контактов с данными."""
        contacts = ["Иван = 123\n", "Мария = 456\n"]
        ContactView.show_contacts(contacts)
        captured = capsys.readouterr()
        assert "СПИСОК КОНТАКТОВ" in captured.out
        assert "1. Иван = 123" in captured.out
        assert "2. Мария = 456" in captured.out
        assert "Всего контактов: 2" in captured.out

    def test_show_contacts_empty(self, capsys):
        """Тест отображения пустого списка контактов."""
        ContactView.show_contacts([])
        captured = capsys.readouterr()
        assert "Справочник пуст" in captured.out

    def test_show_contact_detail_with_data(self, capsys):
        """Тест отображения деталей контакта."""
        ContactView.show_contact_detail("Иван = 123 друг")
        captured = capsys.readouterr()
        assert "ИНФОРМАЦИЯ О КОНТАКТЕ" in captured.out
        assert "Иван = 123 друг" in captured.out

    def test_show_contact_detail_empty(self, capsys):
        """Тест отображения деталей пустого контакта."""
        ContactView.show_contact_detail("")
        captured = capsys.readouterr()
        assert "Контакт не найден" in captured.out

    @patch("builtins.input", side_effect=["Иван", "123", "друг"])
    def test_get_new_contact_data(self, mock_input):
        """Тест получения данных нового контакта."""
        name, number, note = ContactView.get_new_contact_data()
        assert name == "Иван"
        assert number == "123"
        assert note == "друг"

    @patch("builtins.input", side_effect=["", "Иван", "", "123", "друг"])
    def test_get_new_contact_data_with_retry(self, mock_input):
        """Тест получения данных с повторными попытками при пустых полях."""
        name, number, note = ContactView.get_new_contact_data()
        assert name == "Иван"
        assert number == "123"
        assert note == "друг"

    @patch("builtins.input", return_value="Иван")
    def test_get_search_query(self, mock_input):
        """Тест получения поискового запроса."""
        result = ContactView.get_search_query()
        assert result == "Иван"

    @patch("builtins.input", return_value="Иван")
    def test_get_contact_name_for_action(self, mock_input):
        """Тест получения имени контакта для действия."""
        result = ContactView.get_contact_name_for_action("теста")
        assert result == "Иван"

    @patch("builtins.input", side_effect=["Петр", "456", "новый"])
    def test_get_updated_contact_data(self, mock_input):
        """Тест получения обновленных данных контакта."""
        new_name, new_number, new_note = ContactView.get_updated_contact_data()
        assert new_name == "Петр"
        assert new_number == "456"
        assert new_note == "новый"

    def test_exit_programm(self, capsys):
        """Тест выхода из программы."""
        ContactView.exit_programm()
        captured = capsys.readouterr()
        assert "Спасибо за использование программы" in captured.out


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия компонентов."""

    def test_full_contact_lifecycle(self, temp_file_path):
        """Тест полного жизненного цикла контакта."""
        pb = PhoneBook(temp_file_path)

        # Создание
        pb.create_contact("Иван", "123-456", "тест")

        # Поиск
        found = pb.find_contact("Иван")
        assert found is not None
        assert "123-456" in found

        # Изменение
        pb.change_contact("Иван", "Петр", "789-012", "обновлен")
        changed = pb.find_contact("Петр")
        assert changed is not None
        assert "789-012" in changed

        # Удаление
        pb.delete_contact("Петр")
        deleted = pb.find_contact("Петр")
        assert deleted is None

    def test_multiple_contacts(self, temp_file_path):
        """Тест работы с несколькими контактами."""
        pb = PhoneBook(temp_file_path)

        # Создаем несколько контактов
        pb.create_contact("Контакт1", "111", "заметка1")
        pb.create_contact("Контакт2", "222", "заметка2")
        pb.create_contact("Контакт3", "333", "заметка3")

        # Проверяем поиск
        assert pb.find_contact("Контакт1") is not None
        assert pb.find_contact("Контакт2") is not None
        assert pb.find_contact("Контакт3") is not None
        assert pb.find_contact("Контакт4") is None

        # Удаляем средний контакт
        pb.delete_contact("Контакт2")
        assert pb.find_contact("Контакт2") is None
        assert pb.find_contact("Контакт1") is not None
        assert pb.find_contact("Контакт3") is not None

    def test_contact_with_special_characters(self, temp_file_path):
        """Тест создания контакта со специальными символами."""
        pb = PhoneBook(temp_file_path)
        pb.create_contact("Иван-Петр", "+7 (123) 456-78-90", "тест!@#$%")

        found = pb.find_contact("Иван-Петр")
        assert found is not None
        assert "+7 (123) 456-78-90" in found
        assert "тест!@#$%" in found
