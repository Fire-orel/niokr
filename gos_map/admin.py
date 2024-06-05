from django.contrib import admin
from .models import UserManager,TypePublications,Map,Publications

admin.site.register(UserManager)
admin.site.register(TypePublications)
admin.site.register(Map)
admin.site.register(Publications)
# Register your models here.
