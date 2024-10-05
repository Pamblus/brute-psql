import sqlite3
import os
import random
import string

def connect_sqlite3(database):
    try:
        conn = sqlite3.connect(database)
        print("Подключение успешно!")
        return conn
    except sqlite3.Error as err:
        print(f"Ошибка подключения: {err}")
        return None

def show_tables(cursor):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    try:
        cursor.execute(query)
        tables = cursor.fetchall()
        print("Таблицы в базе данных:")
        for table in tables:
            print(table[0])
    except sqlite3.Error as err:
        print(f"Ошибка выполнения запроса: {err}")

def show_table_structure(cursor, table_name):
    query = f"PRAGMA table_info({table_name});"
    try:
        cursor.execute(query)
        columns = cursor.fetchall()
        print(f"Структура таблицы {table_name}:")
        for column in columns:
            print(f"Столбец: {column[1]}, Тип: {column[2]}, Первичный ключ: {column[5]}")
    except sqlite3.Error as err:
        print(f"Ошибка выполнения запроса: {err}")

def show_table_data(cursor, table_name):
    query = f"SELECT * FROM {table_name};"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"Данные таблицы {table_name}:")
        for row in rows:
            print(row)
    except sqlite3.Error as err:
        print(f"Ошибка выполнения запроса: {err}")

def execute_custom_query(cursor):
    query = input("Введите SQL-запрос: ")
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except sqlite3.Error as err:
        print(f"Ошибка выполнения запроса: {err}")

def brute_force_passwords(cursor, table_name, username_column, password_column):
    passwords = ["password", "123456", "admin", "root", ""]
    valid_credentials = []

    for password in passwords:
        query = f"SELECT * FROM {table_name} WHERE {username_column} = 'admin' AND {password_column} = '{password}';"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                valid_credentials.append((result[0], password))
        except sqlite3.Error as err:
            print(f"Ошибка выполнения запроса: {err}")

    if valid_credentials:
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"
        with open(filename, 'w') as f:
            for cred in valid_credentials:
                f.write(f"Username: {cred[0]}, Password: {cred[1]}\n")
        print(f"Валидные учетные данные сохранены в файл: {filename}")
    else:
        print("Валидные учетные данные не найдены.")

def save_all_data(cursor):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    try:
        cursor.execute(query)
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            rows = cursor.fetchall()
            filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"
            with open(filename, 'w') as f:
                f.write(f"Данные таблицы {table_name}:\n")
                for row in rows:
                    f.write(str(row) + "\n")
            print(f"Данные таблицы {table_name} сохранены в файл: {filename}")
    except sqlite3.Error as err:
        print(f"Ошибка выполнения запроса: {err}")

def main():
    database = input("Введите имя базы данных: ")
    conn = connect_sqlite3(database)

    if conn:
        cursor = conn.cursor()
        while True:
            print("\nВыберите действие:")
            print("1. Показать все таблицы")
            print("2. Показать структуру таблицы")
            print("3. Показать данные таблицы")
            print("4. Выполнить произвольный SQL-запрос")
            print("5. Брутфорс паролей")
            print("6. Сохранить все данные в файл")
            print("7. Выход")
            choice = input("Введите номер выбора: ")

            if choice == "1":
                show_tables(cursor)
            elif choice == "2":
                table_name = input("Введите имя таблицы: ")
                show_table_structure(cursor, table_name)
            elif choice == "3":
                table_name = input("Введите имя таблицы: ")
                show_table_data(cursor, table_name)
            elif choice == "4":
                execute_custom_query(cursor)
            elif choice == "5":
                table_name = input("Введите имя таблицы: ")
                username_column = input("Введите имя столбца с именем пользователя: ")
                password_column = input("Введите имя столбца с паролем: ")
                brute_force_passwords(cursor, table_name, username_column, password_column)
            elif choice == "6":
                save_all_data(cursor)
            elif choice == "7":
                break
            else:
                print("Неверный выбор.")

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
