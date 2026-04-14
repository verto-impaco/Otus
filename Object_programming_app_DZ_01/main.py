import os

print("""Меню: 

Введите цифру

1) Создать контакт (введите сначала имя контакта, потом номер телефона и после, по желанию, заметку к нему (по желанию))

2) Найти контакт (введите имя контакта)   

3) Изменить контакт (сначала введите имя контакта, а далее имя и заметку к нему (по желанию))

4) Удалить контакт (введите имя контакта)  

5) Вывести все контакты  

6) Выйти из программы

""")


file_name: str = 'phone_search.txt'

down_programm: bool = False


def create_contact(contact_name, phone_number, note=''):
    """Эта функция создает контакт."""
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f'{contact_name} = {phone_number} {note}\n')
    print('Контакт успешно добавлен')


def find_contact(contact_name):
    """Эта функция ищет контакт."""
    is_found: bool = False
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith(contact_name + ' ='):
                    print(line.strip())
                    is_found = True
                    break
        if is_found == False:
            print('Контакт не найден в справочнике.')
    except FileNotFoundError:
        print("Файл не найден.")


def change_contact(contact_name, new_contact_name, new_contact_number, new_contact_note):
    """Эта функция изменяет контакт."""
    is_found: bool = False
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Файл не найден")
        return

    for i, line in enumerate(lines):
        if line.strip().startswith(contact_name + ' ='):
            lines[i] = f'{new_contact_name} = {new_contact_number} {new_contact_note}\n'
            is_found = True

    if is_found:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            print('Контакт успешно изменен')
    else:
        print('Контакт не найден в справочнике.')


def delete_contact(contact_name):
    """Эта функция удаляет контакт."""
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Файл не найден.")
        return
    new_lines = [line for line in lines if not line.strip(
    ).startswith(contact_name + ' =')]
    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def show_all_contacts():
    """Эта функция выводит все контакты."""
    try:
        if os.path.getsize(file_name) == 0:
            print('В справочнике отсутствуют контакты')
            return
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                print(line)
    except FileNotFoundError:
        print("Файл не найден. Добавьте пожалуйста хотя бы один контакт в справочник")


while down_programm == False:
    command = input("Введите команду: ")
    if str(command) == '6':
        print("Завершение программы...")
        down_programm = True

    elif str(command) == '1':
        contact_name = input('Введите имя контакта: ')
        contact_number = input('Введите телефон контакта: ')
        contact_note = input(
            'Введите заметку (если не хотите, просто нажмите Enter): ')
        create_contact(contact_name, contact_number, contact_note)

    elif str(command) == '2':
        contact_name = input('Введите имя контакта: ')
        find_contact(contact_name)

    elif str(command) == '3':
        contact_name = input('Введите имя контакта: ')
        new_contact_name = input('Введите новое имя контакта: ')
        new_contact_number = input('Введите новый номер контакта: ')
        new_contact_note = input(
            'Введите новую заметку (по желанию, если не хотите, просто нажмите Enter): ')
        change_contact(contact_name, new_contact_name,
                       new_contact_number, new_contact_note)

    elif str(command) == '4':
        show_all_contacts()
        contact_name = input('Введите имя контакта: ')
        delete_contact(contact_name)
        print('Контакт успешно удален')

    elif str(command) == '5':
        show_all_contacts()
    else:
        print(f"Неизвестная команда: {command}")
        continue


print("Программа остановлена.")
