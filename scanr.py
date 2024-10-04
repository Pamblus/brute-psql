import requests
from bs4 import BeautifulSoup
import re

def get_full_url(base_url, path):
    if path.startswith('http://') or path.startswith('https://'):
        return path
    elif path.startswith('/'):
        return base_url.rstrip('/') + path
    else:
        return base_url + path

def analyze_page(url):
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

        print(f"Файл: {url}")
        print(f"Метод: {method}")
        print(f"Ссылка: {action}")
        print(f"Передает: {data}")

        if method == 'POST':
            response = requests.post(action, data=data)
        elif method == 'GET':
            response = requests.get(action, params=data)
        else:
            response = requests.request(method, action, data=data)

        print(f"Получает: {response.text[:100]}...")  # Ограничиваем вывод для краткости
        print(f"Путь: {action}")
        print(f"Файл: {action.split('/')[-1]}")
        print(f"Данные: {response.headers}")
        print()

    # Ищем все ссылки на странице
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        full_href = get_full_url(url, href)
        print(f"Файл: {url}")
        print(f"Метод: GET")
        print(f"Ссылка: {full_href}")
        print(f"Передает: (недоступно без отправки запроса)")
        print(f"Получает: (недоступно без отправки запроса)")
        print(f"Путь: {full_href}")
        print(f"Файл: {full_href.split('/')[-1]}")
        print(f"Данные: (недоступно без отправки запроса)")
        print()

def main():
    # Спрашиваем у пользователя ссылку на источник
    url = input("Введите ссылку на источник (например, http://google.com): ")

    # Добавляем протокол, если он отсутствует
    if not re.match(r'^https?://', url):
        url = 'http://' + url

    # Анализируем страницу
    analyze_page(url)

if __name__ == "__main__":
    main()
