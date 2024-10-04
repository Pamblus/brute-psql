import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from html import escape

def get_full_url(base_url, path):
    return urljoin(base_url, path)

def send_request(method, url, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, params=data)
        elif method == 'POST':
            response = requests.post(url, data=data)
        else:
            response = requests.request(method, url, data=data)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса {method} {url}: {e}")
        return None

def analyze_page(url, visited_urls, base_domain, report_file):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        # Получаем исходный код страницы
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все формы на странице
        forms = soup.find_all('form')
        for form in forms:
            method = form.get('method', 'GET').upper()
            action = form.get('action', url)
            action = get_full_url(url, action)
            inputs = form.find_all('input')
            data = {input.get('name'): input.get('value') for input in inputs}

            print(f"Метод: {method}")
            print(f"Ссылка: {action}")
            if data:
                print(f"Передает: {data}")
                response = send_request(method, action, data)
                if response and 'text/html' not in response.headers.get('Content-Type', ''):
                    print(f"Получает: {response.text[:100]}...")  # Ограничиваем вывод для краткости
                    print(f"Путь: {action}")
                    print(f"Файл: {action.split('/')[-1]}")
                    print(f"Данные: {response.headers}")
                    report_file.write(f"<h3>Метод: {method}</h3>")
                    report_file.write(f"<p>Ссылка: {action}</p>")
                    report_file.write(f"<p>Передает: {escape(str(data))}</p>")
                    report_file.write(f"<p>Получает: {escape(response.text[:100])}...</p>")
                    report_file.write(f"<p>Путь: {action}</p>")
                    report_file.write(f"<p>Файл: {action.split('/')[-1]}</p>")
                    report_file.write(f"<p>Данные: {escape(str(response.headers))}</p>")
                else:
                    print(f"Метод: {method}, Ссылка: {action}")
            else:
                print(f"Метод: {method}, Ссылка: {action}")
            print()

        # Ищем все ссылки на странице
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            full_href = get_full_url(url, href)
            if full_href not in visited_urls:
                if base_domain not in full_href:
                    continue_scan = input(f"Найден другой домен: {full_href}. Продолжить сканирование? (y/n): ")
                    if continue_scan.lower() != 'y':
                        continue
                analyze_page(full_href, visited_urls, base_domain, report_file)

    except Exception as e:
        print(f"Ошибка при анализе {url}: {e}")

def main():
    # Спрашиваем у пользователя ссылку на источник
    url = input("Введите ссылку на источник (например, http://google.com): ")

    # Добавляем протокол, если он отсутствует
    if not re.match(r'^https?://', url):
        url = 'http://' + url

    # Получаем базовый домен
    base_domain = re.search(r'^https?://([^/]+)', url).group(1)

    # Открываем файл для записи отчета
    with open("report.html", "w") as report_file:
        report_file.write("<html><body>")

        # Анализируем страницу
        visited_urls = set()
        analyze_page(url, visited_urls, base_domain, report_file)

        report_file.write("</body></html>")

if __name__ == "__main__":
    main()
