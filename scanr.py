import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def get_full_url(base_url, path):
    return urljoin(base_url, path)

def send_request(method, url, data=None):
    if method == 'GET':
        response = requests.get(url, params=data)
    elif method == 'POST':
        response = requests.post(url, data=data)
    else:
        response = requests.request(method, url, data=data)
    return response

def analyze_page(url, visited_urls):
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
                print(f"Получает: {response.text[:100]}...")  # Ограничиваем вывод для краткости
                print(f"Путь: {action}")
                print(f"Файл: {action.split('/')[-1]}")
                print(f"Данные: {response.headers}")
            else:
                print(f"Метод: {method}, Ссылка: {action}")
            print()

        # Ищем все ссылки на странице
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            full_href = get_full_url(url, href)
            if full_href not in visited_urls:
                analyze_page(full_href, visited_urls)

    except Exception as e:
        print(f"Ошибка при анализе {url}: {e}")

def main():
    # Спрашиваем у пользователя ссылку на источник
    url = input("Введите ссылку на источник (например, http://google.com): ")

    # Добавляем протокол, если он отсутствует
    if not re.match(r'^https?://', url):
        url = 'http://' + url

    # Анализируем страницу
    visited_urls = set()
    analyze_page(url, visited_urls)

if __name__ == "__main__":
    main()
