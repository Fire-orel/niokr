import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
import time

from urllib.parse import urljoin, urlparse, parse_qs


def process_api(base_url, api_key):
    filename = 'result.json'

    url = base_url
    while url:
        # Выполняем запрос к API
        headers = {'Authorization': 'Api-Key ' + api_key}
        response = requests.get(url, headers=headers)

        # Проверяем статус код ответа
        if response.status_code == 200:
            # Получаем данные из ответа
            data = response.json()

            # Проверяем наличие ключа 'results', где хранятся нужные данные
            results = data.get('results', [])

            # Обрабатываем каждую запись и добавляем её в список
            new_data = []
            for item in results:
                full_name = f"{item.get('last_name', '')} {item.get('first_name', '')} {item.get('middle_name', '')}".strip()
                filtered_item = {
                    "full_name": full_name,
                    "last_name": item.get("last_name"),
                    "first_name": item.get("first_name"),
                    "middle_name": item.get("middle_name")
                }
                new_data.append(filtered_item)

            # Загружаем ранее сохраненные данные из файла
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []

            # Объединяем старые и новые данные
            all_data = existing_data + new_data

            # Записываем все данные в файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)

            # Проверяем наличие поля "next" для дополнительных запросов
            next_url = data.get('next')
            if next_url:
                parsed_next = urlparse(next_url)
                query = parsed_next.query

                # Создаем новый URL, добавляя параметры после знака ?
                url = urljoin(base_url, '?' + query)

                # Задержка в 2 секунды перед следующим запросом
                time.sleep(2)
            else:
                url = None
            print(query)
        else:
            # Обрабатываем ошибку
            print('Ошибка при выполнении запроса:', response.status_code)
            return

    print("Результат сохранен в файл 'result.json'")
url = 'https://cabinet.zabgu.ru/api/v1/physical-person/'
api_key = os.getenv("api_key")

process_api(url, api_key)
