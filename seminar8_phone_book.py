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
import datetime as dt

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


def file_extension(file_name):
    return file_name.split(".")[-1] if file_name.count(".") > 0 else ""


def file_without_extension(file_name):
    return ".".join(file_name.split(".")[:-1]) if file_name.count(".") > 0 else file_name


def get_info(mode_editing=False):
    data = []
    data.append(correct_name("Фамилия: ", max_len_name=45))
    data.append(correct_name("Имя: "))
    data.append(correct_name("Отчество: "))
    phone = correct_number("Телефон в формате (от 3 до 11 цифр): ", min_len_name=3, max_len_name=11)
    existing_phones = search_records(file_name, str(phone), True)
    if not mode_editing:
        existing_phones = search_records(file_name, str(phone), True)        
        while len(existing_phones) > 0:
            print("Такой телефон зарегестрирован на", end=" ")
            print_list_formatting(existing_phones)
            phone = correct_number("Телефон в формате (от 3 до 11 цифр): ", min_len_name=3, max_len_name=11)
            existing_phones = search_records(file_name, str(phone), True)
    data.append(phone)
    return data


def field_names():
    return ["Фамилия","Имя","Отчество","Телефон"]


def create_file(file_name):
    with open(file_name, "w", encoding="utf-8") as pb:
        f_writer = DictWriter(pb, field_names())
        f_writer.writeheader()


def backup(file_name):
    backup_file_name = (file_without_extension(file_name) + "_" +
        str(dt.datetime.now())[:19].replace("-", "").replace(" ", "_").replace(":", "") +
        ".csv")
    create_file(backup_file_name)
    data_to_write = [items[1] for items in read_file(file_name)]
    write_file(backup_file_name, data_to_write)
    print(f"Создан резерный файл: {backup_file_name}")


def set_of_backup_to_delete(file_name):
    extension_of_file = file_extension(file_name)
    name_of_file = file_without_extension(file_name)
    all_files = set(filter(lambda el: str(el).endswith(extension_of_file) and str(el).startswith(name_of_file), os.listdir(os.getcwd())))
    excluded_files = set([file_name, max([os.path.getatime(os.getcwd() + os.sep + f) for f in all_files])])
    return all_files - excluded_files


def delete_old_backup(file_name):
    path_to_delete = os.getcwd() + os.sep
    set_of_file_to_delete = set_of_backup_to_delete(file_name)
    for cur_file in set_of_file_to_delete:
        file_to_delete = path_to_delete + cur_file
        os.remove(file_to_delete)
        print(f"Удален более не нужный резерный файл: {file_to_delete}")


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


def search_records(file_name, to_find, accurate_search=False):
    phone_book = read_file(file_name)
    searched_records = []
    if accurate_search:
        for item in phone_book:
            for v in item[1].values():
                if str(to_find).lower() == str(v).lower():
                    if item not in searched_records:
                        searched_records.append(item)
    else:
        for item in phone_book:
            for v in item[1].values():
                if str(to_find).lower() in str(v).lower():
                    if item not in searched_records:
                        searched_records.append(item)
    return searched_records


def edit_record(file_name, to_find):
    changed = False
    phone_book = read_file(file_name)
    for el in phone_book:
        for v in el[1].values():
            if to_find.lower() == str(v).lower():
                print_list_formatting([el])
                if input("Редактировать запись? (y - да)").lower() != "y":
                    continue
                changed = True
                data = get_info(True)
                el[1]["Фамилия"] = data[0]
                el[1]["Имя"] = data[1]
                el[1]["Отчество"] = data[2]
                el[1]["Телефон"] = data[3]
                print("Запись отредактирована: ", end=" ")
                print_list_formatting([el])
    if changed:
        data_to_write = [items[1] for items in phone_book]
        write_file(file_name, data_to_write)


def delete_record(file_name, to_find):
    changed = False
    phone_book = read_file(file_name)
    for el in phone_book:
        for v in el[1].values():
            if to_find.lower() == v.lower():
                print_list_formatting([el])
                if input("Удалить запись? (y - да)").lower() != "y":
                    continue
                changed = True
                print("Запись удалена: ", end=" ")
                print_list_formatting([phone_book.pop(phone_book.index(el))])
    if changed:
        data_to_write = [items[1] for items in phone_book]
        write_file(file_name, data_to_write)


def main():

    if not os.path.exists(file_name):
        create_file(file_name)
    else:
        delete_old_backup(file_name)
        backup(file_name)

    while True:
        command = input("Введите команду для работы с телефонным справочником (q-выход, p-печать, w-новая запись, e-редактировать запись, d-удалить запись, s-поиск значения): ").lower()

        if command == "q": # 0 Выйти из цикла
            break
        elif command == "p": # 1 Выводить данные
            print_list_formatting(read_file(file_name))
        elif command == "w": # Добавить данные
            add_records(file_name, [get_info()])
        elif command == "e":  # Редактировать данные
            edit_record(file_name, input("Найти строки для редактирования (по полному совпадению (фамилия или имя или отчество или телефон)): "))
        elif command == "d": # Удалить данные
            delete_record(file_name, input("Найти строки для удаления (по полному совпадению (фамилия или имя или отчество или телефон)): "))
        elif command == "s":  # Искать данные
            print_list_formatting(search_records(file_name, input("Введите поисковую строку (по частичному совпадению): ")))
        else:
            print(f"Команды '{command}' нет! ")

    print("Завершение программы...")


main()