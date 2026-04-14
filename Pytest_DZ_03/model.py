from dataclasses import dataclass
import os
from typing import List, Optional


PATH: str = 'phone_search.txt'


@dataclass
class Contact:
    name: str
    number: str
    note: str = ''


class FileWrite:
    @staticmethod
    def file_write(path, to_write):
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.writelines(to_write)
        except FileNotFoundError:
            print("Файл не найден.")

    @staticmethod
    def file_append(path, to_append):
        try:
            with open(path, 'a', encoding='utf-8') as file:
                file.write(to_append)
        except FileNotFoundError:
            print("Файл не найден.")


class FileRead:
    @staticmethod
    def file_read(path: str) -> Optional[List[str]]:
        lines: List[str] = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line)
        return lines


class PhoneBook:

    def __init__(self, file_path: str = PATH):
        self.path = file_path

    def create_contact(self, name: str, number: str, note: str = ''):
        """Этот метод создает контакт."""
        self._contact = Contact(name, number, note)
        FileWrite.file_append(
            self.path, f'{self._contact.name} = {self.path, self._contact.number} {self._contact.note}\n')

    def find_contact(self, contact_name) -> Optional[str]:
        """Этот метод ищет контакт."""
        lines = FileRead.file_read(self.path)
        if lines is None:
            return None
        for line in lines:
            if line.startswith(contact_name + ' ='):
                return line.strip()

    def change_contact(self, contact_name: str, new_contact_name: str, new_contact_number: str, new_contact_note: str):
        """Этот метод изменяет контакт."""
        is_found: bool = False
        lines = FileRead.file_read(self.path)

        if lines is None:
            print("Файл не найден или пуст")
            return is_found

        for i, line in enumerate(lines):
            if line.strip().startswith(contact_name + ' ='):
                lines[i] = f'{new_contact_name} = {new_contact_number} {new_contact_note}\n'
                is_found = True

        if is_found:
            FileWrite.file_write(self.path, lines)
            print('Контакт успешно изменен')
        else:
            print('Контакт не найден в справочнике.')

    def delete_contact(self, contact_name):
        """Этот метод удаляет контакт."""
        lines = FileRead.file_read(self.path)

        if lines is None:
            print(f"Не удалось прочитать файл {self.path}")
            return False

        new_lines = [line for line in lines if not line.strip(
        ).startswith(contact_name + ' =')]
        FileWrite.file_write(self.path, new_lines)

    def show_all_contacts(self):
        """Эта функция выводит все контакты."""
        if os.path.getsize(self.path) == 0:
            print('В справочнике отсутствуют контакты')
        else:
            print(FileRead.file_read(self.path))
