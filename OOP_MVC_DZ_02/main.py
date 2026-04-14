from controller import PhoneBookController


def main():
    """Основная функция запуска программы"""
    print("Запуск телефонного справочника...")

    controller = PhoneBookController()
    controller.run()

    print("Программа завершена.")


if __name__ == "__main__":
    main()
