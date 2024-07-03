from django.core.cache import cache
from gos_map.models import FullNameАuthor

def get_cached_authors():
    authors = cache.get('authors')
    if not authors:
        authors = FullNameАuthor.objects.all()
        cache.set('authors', authors, 60*60)  # Кэшировать на 1 час
        print("ok")
    return authors
