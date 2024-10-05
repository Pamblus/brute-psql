import mysql.connector
import pymysql
import sqlite3

def connect_mysql_connector(host, user, password, port, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        print("Подключение успешно!")
        return conn
    except mysql.connector.Error as err:
        print(f"Ошибка подключения: {err}")
        return None

def connect_pymysql(host, user, password, port, database):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        print("Подключение успешно!")
        return conn
    except pymysql.MySQLError as err:
        print(f"Ошибка подключения: {err}")
        return None

def connect_sqlite3(database):
    try:
        conn = sqlite3.connect(database)
        print("Подключение успешно!")
        return conn
    except sqlite3.Error as err:
        print(f"Ошибка подключения: {err}")
        return None

def main():
    print("Выберите библиотеку для подключения:")
    print("1. mysql-connector-python")
    print("2. pymysql")
    print("3. sqlite3")
    choice = input("Введите номер выбора: ")

    host = input("Введите IP-адрес или домен: ")
    user = input("Введите имя пользователя: ")
    password = input("Введите пароль (оставьте пустым, если без пароля): ")
    port = input("Введите порт (оставьте пустым для стандартного): ")
    database = input("Введите имя базы данных: ")

    if port == "":
        port = 3306
    else:
        port = int(port)

    if choice == "1":
        conn = connect_mysql_connector(host, user, password, port, database)
    elif choice == "2":
        conn = connect_pymysql(host, user, password, port, database)
    elif choice == "3":
        conn = connect_sqlite3(database)
    else:
        print("Неверный выбор.")
        return

    if conn:
        cursor = conn.cursor()
        while True:
            query = input("Введите SQL-запрос (или 'exit' для выхода): ")
            if query.lower() == 'exit':
                break
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    print(row)
            except Exception as e:
                print(f"Ошибка выполнения запроса: {e}")
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
