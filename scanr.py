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

        print(f"[имя файла в котором найдено] {url}")
        print(f"[название метода] {method}")
        print(f"[куда ссылается] {action}")
        print(f"[что передаёт] {data}")
        print(f"[что получает] (недоступно без отправки запроса)")
        print(f"[путь ссылки] {action}")
        print(f"[имя ссылаемого файла] (недоступно без отправки запроса)")
        print(f"[другие данные] (недоступно без отправки запроса)")
        print()

    # Ищем все ссылки на странице
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        full_href = get_full_url(url, href)
        print(f"[имя файла в котором найдено] {url}")
        print(f"[название метода] GET")
        print(f"[куда ссылается] {full_href}")
        print(f"[что передаёт] (недоступно без отправки запроса)")
        print(f"[что получает] (недоступно без отправки запроса)")
        print(f"[путь ссылки] {full_href}")
        print(f"[имя ссылаемого файла] (недоступно без отправки запроса)")
        print(f"[другие данные] (недоступно без отправки запроса)")
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
