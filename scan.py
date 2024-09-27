import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import sys

def clear_screen():
    """
    Очищает экран терминала.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """
    Выводит красивое название PAMBLUS.
    """
    banner = """
██████████████████████████████████████████████
█▄─▄▄─██▀▄─██▄─▀█▀─▄█▄─▄─▀█▄─▄███▄─██─▄█─▄▄▄▄█
██─▄▄▄██─▀─███─█▄█─███─▄─▀██─██▀██─██─██▄▄▄▄─█
▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▄▀
"""
    print(banner)

def install_dependencies():
    """
    Устанавливает необходимые библиотеки, если они отсутствуют.
    """
    required_packages = ['requests', 'beautifulsoup4']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Устанавливаем {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def get_host_info(target):
    """
    Получает информацию о хосте с помощью nmap.
    :param target: IP-адрес или домен цели.
    :return: Словарь с информацией о хосте.
    """
    nmap_command = f"nmap -sV -O {target}"
    result = subprocess.run(nmap_command, shell=True, capture_output=True, text=True)
    return result.stdout

def scan_ports(target):
    """
    Сканирует открытые порты на целевом хосте.
    :param target: IP-адрес или домен цели.
    :return: Список открытых портов.
    """
    nmap_command = f"nmap -p- {target}"
    result = subprocess.run(nmap_command, shell=True, capture_output=True, text=True)
    open_ports = []
    for line in result.stdout.splitlines():
        if '/tcp' in line or '/udp' in line:
            port = line.split('/')[0]
            open_ports.append(port)
    return open_ports

def dirb_scan(target):
    """
    Сканирует файлы и папки на целевом сайте с помощью dirb.
    :param target: IP-адрес или домен цели.
    :return: Список найденных файлов и папок.
    """
    dirb_command = f"dirb http://{target} /usr/share/dirb/wordlists/common.txt"
    result = subprocess.run(dirb_command, shell=True, capture_output=True, text=True)
    found_items = []
    for line in result.stdout.splitlines():
        if '+ ' in line:
            found_items.append(line.split(' ')[-1])
    return found_items

def find_links_and_keywords(url):
    """
    Ищет ссылки и ключевые слова на целевом сайте.
    :param url: URL цели.
    :return: Список найденных ссылок и ключевых слов.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    keywords = []
    
    # Ищем ссылки
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(('http://', 'https://')):
            links.append(href)
    
    # Ищем ключевые слова
    text = soup.get_text()
    for word in ['admin', 'administrator', 'user', 'database', 'login', 'password']:
        if word in text:
            keywords.append(word)
    
    return links, keywords

def find_requests(url):
    """
    Ищет POST и GET запросы на целевом сайте.
    :param url: URL цели.
    :return: Список найденных запросов.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    requests_found = []
    
    # Ищем GET запросы
    for form in soup.find_all('form'):
        method = form.get('method', 'GET').upper()
        if method == 'GET':
            requests_found.append(f"GET: {form.get('action')}")
    
    # Ищем POST запросы
    for form in soup.find_all('form'):
        method = form.get('method', 'GET').upper()
        if method == 'POST':
            requests_found.append(f"POST: {form.get('action')}")
    
    return requests_found

def scan_security_headers(url):
    """
    Сканирует на наличие заголовков безопасности.
    :param url: URL цели.
    :return: Список найденных заголовков безопасности.
    """
    response = requests.get(url)
    security_headers = []
    for header in response.headers:
        if header.lower() in ['x-frame-options', 'x-xss-protection', 'x-content-type-options', 'strict-transport-security', 'content-security-policy']:
            security_headers.append(f"{header}: {response.headers[header]}")
    return security_headers

def scan_directory_listing(url):
    """
    Сканирует на наличие открытых директорий.
    :param url: URL цели.
    :return: Список найденных открытых директорий.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    directory_listing = []
    if soup.find('pre'):
        directory_listing.append(url)
    return directory_listing

def scan_ssl_tls(target):
    """
    Сканирует на наличие уязвимостей в SSL/TLS.
    :param target: IP-адрес или домен цели.
    :return: Результат сканирования.
    """
    sslscan_command = f"sslscan {target}"
    result = subprocess.run(sslscan_command, shell=True, capture_output=True, text=True)
    return result.stdout

def scan_cms_vulnerabilities(target):
    """
    Сканирует на наличие уязвимостей в CMS (например, WordPress, Joomla).
    :param target: IP-адрес или домен цели.
    :return: Результат сканирования.
    """
    wpscan_command = f"wpscan --url http://{target}"
    result = subprocess.run(wpscan_command, shell=True, capture_output=True, text=True)
    return result.stdout

def scan_web_server_vulnerabilities(target):
    """
    Сканирует на наличие уязвимостей в веб-сервере (например, Apache, Nginx).
    :param target: IP-адрес или домен цели.
    :return: Результат сканирования.
    """
    nikto_command = f"nikto -h {target}"
    result = subprocess.run(nikto_command, shell=True, capture_output=True, text=True)
    return result.stdout

def show_progress(message, duration=2):
    """
    Показывает прогресс выполнения задачи.
    :param message: Сообщение для отображения.
    :param duration: Продолжительность отображения.
    """
    print(message, end='', flush=True)
    for _ in range(duration):
        time.sleep(1)
        print('.', end='', flush=True)
    print()

def main():
    clear_screen()
    print_banner()
    install_dependencies()
    
    target = input("Введите IP-адрес или домен цели (например, google.com): ")
    
    # Убираем http:// или https://, если они есть
    if target.startswith(('http://', 'https://')):
        target = target.split('//')[1]
    
    show_progress("Сканируем хост")
    host_info = get_host_info(target)
    print(host_info)
    
    show_progress("Сканируем открытые порты")
    open_ports = scan_ports(target)
    print(f"Открытые порты: {open_ports}")
    
    show_progress("Сканируем файлы и папки")
    found_items = dirb_scan(target)
    print(f"Найденные файлы и папки: {found_items}")
    
    show_progress("Ищем ссылки и ключевые слова")
    links, keywords = find_links_and_keywords(f"http://{target}")
    print(f"Найденные ссылки: {links}")
    print(f"Найденные ключевые слова: {keywords}")
    
    show_progress("Ищем POST и GET запросы")
    requests_found = find_requests(f"http://{target}")
    print(f"Найденные запросы: {requests_found}")
    
    show_progress("Сканируем на наличие заголовков безопасности")
    security_headers = scan_security_headers(f"http://{target}")
    print(f"Найденные заголовки безопасности: {security_headers}")
    
    show_progress("Сканируем на наличие открытых директорий")
    directory_listing = scan_directory_listing(f"http://{target}")
    print(f"Найденные открытые директории: {directory_listing}")
    
    show_progress("Сканируем на наличие уязвимостей в SSL/TLS")
    ssl_tls_vulnerabilities = scan_ssl_tls(target)
    print(ssl_tls_vulnerabilities)
    
    show_progress("Сканируем на наличие уязвимостей в CMS")
    cms_vulnerabilities = scan_cms_vulnerabilities(target)
    print(cms_vulnerabilities)
    
    show_progress("Сканируем на наличие уязвимостей в веб-сервере")
    web_server_vulnerabilities = scan_web_server_vulnerabilities(target)
    print(web_server_vulnerabilities)
    
    # Собираем все данные в таблицу
    data = {
        "Host Info": host_info,
        "Open Ports": open_ports,
        "Found Items": found_items,
        "Links": links,
        "Keywords": keywords,
        "Requests": requests_found,
        "Security Headers": security_headers,
        "Directory Listing": directory_listing,
        "SSL/TLS Vulnerabilities": ssl_tls_vulnerabilities,
        "CMS Vulnerabilities": cms_vulnerabilities,
        "Web Server Vulnerabilities": web_server_vulnerabilities
    }
    
    # Выводим данные в таблицу
    print("\nРезультаты сканирования:")
    for key, value in data.items():
        print(f"{key}: {value}")
    
    # Предлагаем сохранить результаты
    save_option = input("Сохранить результаты в файл? (y/n): ")
    if save_option.lower() == 'y':
        file_format = input("Выберите формат файла (txt/csv): ")
        if file_format.lower() == 'txt':
            with open("pamblus_results.txt", "w") as f:
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
            print("Результаты сохранены в pamblus_results.txt")
        elif file_format.lower() == 'csv':
            with open("pamblus_results.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Category", "Data"])
                for key, value in data.items():
                    writer.writerow([key, value])
            print("Результаты сохранены в pamblus_results.csv")
        else:
            print("Неизвестный формат файла. Результаты не сохранены.")

if __name__ == "__main__":
    main()
