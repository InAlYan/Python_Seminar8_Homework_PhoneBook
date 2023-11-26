# Задача №49. Решение в группах
# Создать телефонный справочник с возможностью импорта и экспорта данных в формате .txt.
# Фамилия, имя, отчество, номер телефона - данные, которые должны находиться в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в текстовом файле
# 3. Пользователь может ввести одну из характеристик для поиска определенной записи(Например имя или фамилию человека)
# 4. Использование функций. Ваша программа не должна быть линейной

# Задача 38: Дополнить телефонный справочник возможностью изменения и удаления данных.
# Пользователь также может ввести имя или фамилию, и Вы должны реализовать функционал для изменения и удаления данных.

# Дополнить справочник возможностью копирования данных из одного файла в другой. Пользователь вводит номер строки, 
# которую необходимо перенести из одного файла в другой.

from csv import DictReader, DictWriter
import os

file_name = "phone_book.csv"


def is_chars_in_string_in_set(in_str, char_set):
    return set(char_set) > set(in_str.lower())


def is_russian_vovels(in_str):
    return bool(set("аеёиоуыэюя") & set(in_str.lower()))


def correct_name(prompt_to_user, min_len_name=2, max_len_name=20):
    name = input(prompt_to_user).strip()
    while (not is_chars_in_string_in_set(name, "абвгдеёжзийклмнопрстуфхцчшщъыьэюя-") or not is_russian_vovels(name)
           or len(name) < min_len_name or len(name) > max_len_name):
        name = input("Не корректно!!! Повторите " + prompt_to_user).strip()
    else:
        return name.capitalize()


def correct_number(prompt_to_user, min_len_name=3, max_len_name=11):
    num = input(prompt_to_user).strip()
    while not num.isnumeric() or len(num) < min_len_name or len(num) > max_len_name:
        num = input("Неверный номер!!! " + prompt_to_user).strip()
    else:
        return int(num)


def get_info(mode_editing=False):
    data = []
    data.append(correct_name("Фамилия: ", max_len_name=45))
    data.append(correct_name("Имя: "))
    data.append(correct_name("Отчество: "))
    phone = correct_number("Телефон в формате (от 3 до 11 цифр): ", min_len_name=3, max_len_name=11)

    data.append(phone)
    return data


def field_names():
    return ["Фамилия","Имя","Отчество","Телефон"]


def create_file(file_name):
    with open(file_name, "w", encoding="utf-8") as pb:
        f_writer = DictWriter(pb, field_names())
        f_writer.writeheader()


def write_file(file_name, lst_to_file):
    with open(file_name, "w", encoding="utf-8", newline="") as pb:
        f_writer = DictWriter(pb, field_names())
        f_writer.writeheader()
        f_writer.writerows(lst_to_file)


def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as pb:
        f_reader = DictReader(pb)
        res = [(ind, el) for ind, el in enumerate(f_reader)]
    return res


def print_list_formatting(phone_lst):
    for items in phone_lst:
        print(f"{items[0]} {items[1]['Фамилия']} {items[1]['Имя']} {items[1]['Отчество']} : телефон {items[1]['Телефон']}")


def add_records(file_name, fio_phone_records):
    with open(file_name, "r", encoding="utf-8") as pb:
        f_reader = DictReader(pb)
        res = list(f_reader)
    for el in fio_phone_records:
        obj = dict(zip(field_names(), el))
        res.append(obj)
    write_file(file_name, res)


def main():

    if not os.path.exists(file_name):
        create_file(file_name)

    while True:
        command = input("Введите команду для работы с телефонным справочником (q-выход, p-печать, w-новая запись: ").lower()

        if command == "q": # 0 Выйти из цикла
            break
        elif command == "p": # 1 Выводить данные
            print_list_formatting(read_file(file_name))
        elif command == "w": # Добавить данные
            add_records(file_name, [get_info()])
        else:
            print(f"Команды '{command}' нет! ")

    print("Завершение программы...")


main()