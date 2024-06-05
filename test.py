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




if len(quarter)!=0:
            for i in quarter:
                workbook = Workbook()
                workbook.remove(workbook.active)
                map_date=Map.objects.filter(quarter=i)
                map_list.append(map_date[0])

                for o in table:
                    if o == 'publication':

                        count=2
                        sheet = workbook.create_sheet('Публикации')
                        sheet['A1']="Тип публикации"
                        sheet['B1']="ФИО автора"
                        sheet['C1']="Наименование публикации"
                        sheet['D1']="Выходные данные публикации (Название журнала, Номер, Том, страницы)"
                        sheet['E1']="Год"
                        sheet['F1']="Место опубликования"
                        sheet['G1']="Объем публикации (п.л.)"
                        sheet['H1']="eLIBRARY ID"
                        sheet['I1']="DOI публикации"



                        for q in map_date:
                            if not len(type_table_publication)>0:
                                publications=Publications.objects.filter(id_map=q)
                                for u in publications:
                                    sheet[f"A{count}"]=u.type_publication.name_type_publications
                                    sheet[f"B{count}"]=u.full_name_author
                                    sheet[f"C{count}"]=u.name_publication
                                    sheet[f"D{count}"]=u.exit_data
                                    sheet[f"E{count}"]=u.year
                                    sheet[f"F{count}"]=u.place_publication
                                    sheet[f"G{count}"]=u.volume_publication
                                    sheet[f"H{count}"]=u.eLIBRARY_ID
                                    sheet[f"I{count}"]=u.doi_publication
                                    count+=1

                            else:
                                for u in type_table_publication:
                                    publications=Publications.objects.filter(id_map=q,type_publication=u)
                                    for w in publications:
                                        sheet[f"A{count}"]=w.type_publication.name_type_publications
                                        sheet[f"B{count}"]=w.full_name_author
                                        sheet[f"C{count}"]=w.name_publication
                                        sheet[f"D{count}"]=w.exit_data
                                        sheet[f"E{count}"]=w.year
                                        sheet[f"F{count}"]=w.place_publication
                                        sheet[f"G{count}"]=w.volume_publication
                                        sheet[f"H{count}"]=w.eLIBRARY_ID
                                        sheet[f"I{count}"]=w.doi_publication
                                        count+=1

                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename=example.xlsx'

                # Сохраняем книгу в объект HttpResponse
                workbook.save(response)

                # Возвращаем HTTP-ответ с загруженным файлом
                return response
        else:
            workbook = Workbook()
            workbook.remove(workbook.active)
            map_date=Map.objects.filter()
            map_list.append(map_date[0])

            for o in table:
                if o == 'publication':

                    count=2
                    sheet = workbook.create_sheet('Публикации')
                    sheet['A1']="Тип публикации"
                    sheet['B1']="ФИО автора"
                    sheet['C1']="Наименование публикации"
                    sheet['D1']="Выходные данные публикации (Название журнала, Номер, Том, страницы)"
                    sheet['E1']="Год"
                    sheet['F1']="Место опубликования"
                    sheet['G1']="Объем публикации (п.л.)"
                    sheet['H1']="eLIBRARY ID"
                    sheet['I1']="DOI публикации"



                    for q in map_date:
                        if not len(type_table_publication)>0:
                            publications=Publications.objects.filter(id_map=q)
                            for u in publications:
                                sheet[f"A{count}"]=u.type_publication.name_type_publications
                                sheet[f"B{count}"]=u.full_name_author
                                sheet[f"C{count}"]=u.name_publication
                                sheet[f"D{count}"]=u.exit_data
                                sheet[f"E{count}"]=u.year
                                sheet[f"F{count}"]=u.place_publication
                                sheet[f"G{count}"]=u.volume_publication
                                sheet[f"H{count}"]=u.eLIBRARY_ID
                                sheet[f"I{count}"]=u.doi_publication
                                count+=1

                        else:
                            for u in type_table_publication:
                                publications=Publications.objects.filter(id_map=q,type_publication=u)
                                for w in publications:
                                    sheet[f"A{count}"]=w.type_publication.name_type_publications
                                    sheet[f"B{count}"]=w.full_name_author
                                    sheet[f"C{count}"]=w.name_publication
                                    sheet[f"D{count}"]=w.exit_data
                                    sheet[f"E{count}"]=w.year
                                    sheet[f"F{count}"]=w.place_publication
                                    sheet[f"G{count}"]=w.volume_publication
                                    sheet[f"H{count}"]=w.eLIBRARY_ID
                                    sheet[f"I{count}"]=w.doi_publication
                                    count+=1

                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=example.xlsx'

                # Сохраняем книгу в объект HttpResponse
                workbook.save(response)

                # Возвращаем HTTP-ответ с загруженным файлом
                return response

