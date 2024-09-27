import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import sys
import random
import string

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

def scan_robots_txt(target):
    """
    Сканирует файл robots.txt на целевом сайте.
    :param target: IP-адрес или домен цели.
    :return: Содержимое файла robots.txt.
    """
    robots_url = f"http://{target}/robots.txt"
    response = requests.get(robots_url)
    if response.status_code == 200:
        return response.text
    else:
        return "Файл robots.txt не найден."

def scan_sitemap_xml(target):
    """
    Сканирует файл sitemap.xml на целевом сайте.
    :param target: IP-адрес или домен цели.
    :return: Содержимое файла sitemap.xml.
    """
    sitemap_url = f"http://{target}/sitemap.xml"
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        return response.text
    else:
        return "Файл sitemap.xml не найден."

def scan_admin_panel(target):
    """
    Сканирует на наличие панели администратора на целевом сайте.
    :param target: IP-адрес или домен цели.
    :return: URL панели администратора, если найдена.
    """
    admin_paths = ['/admin', '/login', '/wp-admin', '/administrator']
    for path in admin_paths:
        admin_url = f"http://{target}{path}"
        response = requests.get(admin_url)
        if response.status_code == 200:
            return admin_url
    return "Панель администратора не найдена."

def scan_error_pages(target):
    """
    Сканирует на наличие страниц ошибок на целевом сайте.
    :param target: IP-адрес или домен цели.
    :return: Список найденных страниц ошибок.
    """
    error_pages = []
    for code in [400, 401, 403, 404, 500]:
        error_url = f"http://{target}/{code}.html"
        response = requests.get(error_url)
        if response.status_code == 200:
            error_pages.append(error_url)
    return error_pages

def scan_http_methods(target):
    """
    Сканирует поддерживаемые HTTP методы на целевом сайте.
    :param target: IP-адрес или домен цели.
    :return: Список поддерживаемых HTTP методов.
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
    supported_methods = []
    for method in methods:
        response = requests.request(method, f"http://{target}")
        if response.status_code != 405:
            supported_methods.append(method)
    return supported_methods

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

def generate_random_string(length=5):
    """
    Генерирует случайную строку из букв и цифр.
    :param length: Длина строки.
    :return: Случайная строка.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
    
    show_progress("Сканируем файл robots.txt")
    robots_txt = scan_robots_txt(target)
    print(f"Содержимое robots.txt: {robots_txt}")
    
    show_progress("Сканируем файл sitemap.xml")
    sitemap_xml = scan_sitemap_xml(target)
    print(f"Содержимое sitemap.xml: {sitemap_xml}")
    
    show_progress("Сканируем на наличие панели администратора")
    admin_panel = scan_admin_panel(target)
    print(f"Панель администратора: {admin_panel}")
    
    show_progress("Сканируем на наличие страниц ошибок")
    error_pages = scan_error_pages(target)
    print(f"Найденные страницы ошибок: {error_pages}")
    
    show_progress("Сканируем поддерживаемые HTTP методы")
    http_methods = scan_http_methods(target)
    print(f"Поддерживаемые HTTP методы: {http_methods}")
    
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
        "Web Server Vulnerabilities": web_server_vulnerabilities,
        "Robots.txt": robots_txt,
        "Sitemap.xml": sitemap_xml,
        "Admin Panel": admin_panel,
        "Error Pages": error_pages,
        "HTTP Methods": http_methods
    }
    
    # Выводим данные в таблицу
    print("\nРезультаты сканирования:")
    for key, value in data.items():
        print(f"{key}: {value}")
    
    # Предлагаем сохранить результаты
    save_option = input("Сохранить результаты в файл? (y/n): ")
    if save_option.lower() == 'y':
        file_format = input("Выберите формат файла (txt/csv): ")
        random_suffix = generate_random_string()
        if file_format.lower() == 'txt':
            filename = f"pamblus_results_{random_suffix}.txt"
            with open(filename, "w") as f:
                f.write(f"Сканирование сайта: {target}\n\n")
                for key, value in data.items():
                    f.write(f"{key}:\n{value}\n\n")
            print(f"Результаты сохранены в {filename}")
        elif file_format.lower() == 'csv':
            filename = f"pamblus_results_{random_suffix}.csv"
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Category", "Data"])
                for key, value in data.items():
                    writer.writerow([key, value])
            print(f"Результаты сохранены в {filename}")
        else:
            print("Неизвестный формат файла. Результаты не сохранены.")

if __name__ == "__main__":
    main()
