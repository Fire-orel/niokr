import json
import os
import django

# Настройте окружение Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niokr.settings')
django.setup()

from gos_map.models import FullNameАuthor

# Путь к вашему JSON файлу
file_path = 'media/json/result.json'

# Загрузка данных из JSON файла
# with open(file_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)
#     for item in data:
#         model_instance = FullNameАuthor.objects.create(

#             full_name=item['text']
#             )

#         model_instance.save()
#         print(item)


print(FullNameАuthor.objects.all())
