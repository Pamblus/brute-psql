import mysql.connector

def connect_mysql(host, user, password, port):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        print("Подключение успешно!")
        return conn
    except mysql.connector.Error as err:
        print(f"Ошибка подключения: {err}")
        return None

def show_databases(cursor):
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("Список баз данных:")
    for db in databases:
        print(db[0])

def show_tables(cursor, database):
    cursor.execute(f"USE {database}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"Список таблиц в базе данных '{database}':")
    for table in tables:
        print(table[0])

def show_table_structure(cursor, database, table):
    cursor.execute(f"USE {database}")
    cursor.execute(f"DESCRIBE {table}")
    structure = cursor.fetchall()
    print(f"Структура таблицы '{table}' в базе данных '{database}':")
    for column in structure:
        print(column)

def show_table_data(cursor, database, table):
    cursor.execute(f"USE {database}")
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    print(f"Данные таблицы '{table}' в базе данных '{database}':")
    for row in data:
        print(row)

def execute_query(cursor, database, query):
    cursor.execute(f"USE {database}")
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as err:
        print(f"Ошибка выполнения запроса: {err}")

def main():
    host = input("Введите IP-адрес или домен: ")
    user = input("Введите имя пользователя: ")
    password = input("Введите пароль (оставьте пустым, если без пароля): ")
    port = input("Введите порт (оставьте пустым для стандартного): ")

    if port == "":
        port = 3306
    else:
        port = int(port)

    conn = connect_mysql(host, user, password, port)
    if conn:
        cursor = conn.cursor()
        
        while True:
            print("\nВыберите действие:")
            print("1. Показать все базы данных")
            print("2. Выбрать базу данных")
            print("3. Выход")
            choice = input("Введите номер выбора: ")

            if choice == "1":
                show_databases(cursor)
            elif choice == "2":
                database = input("Введите имя базы данных: ")
                cursor.execute(f"USE {database}")
                while True:
                    print("\nВыберите действие:")
                    print("1. Показать все таблицы")
                    print("2. Показать структуру таблицы")
                    print("3. Показать данные таблицы")
                    print("4. Выполнить произвольный SQL-запрос")
                    print("5. Вернуться к выбору базы данных")
                    sub_choice = input("Введите номер выбора: ")

                    if sub_choice == "1":
                        show_tables(cursor, database)
                    elif sub_choice == "2":
                        table = input("Введите имя таблицы: ")
                        show_table_structure(cursor, database, table)
                    elif sub_choice == "3":
                        table = input("Введите имя таблицы: ")
                        show_table_data(cursor, database, table)
                    elif sub_choice == "4":
                        query = input("Введите SQL-запрос: ")
                        execute_query(cursor, database, query)
                    elif sub_choice == "5":
                        break
                    else:
                        print("Неверный выбор.")
            elif choice == "3":
                break
            else:
                print("Неверный выбор.")

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
