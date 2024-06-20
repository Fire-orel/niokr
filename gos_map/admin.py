from django.contrib import admin
from .models import UserManager,TypePublications,Map,Publications,TypeDocuments,TypeProperty,SecurityDocuments,TypeMonographs,Monographs

admin.site.register(UserManager)
admin.site.register(TypePublications)
admin.site.register(Map)
admin.site.register(Publications)
admin.site.register(TypeDocuments)
admin.site.register(TypeProperty)
admin.site.register(SecurityDocuments)
admin.site.register(TypeMonographs)
admin.site.register(Monographs)
# Register your models here.
