from django.contrib import admin
from .models import UserManager,TypePublications,Map,Publications,TypeDocuments,TypeProperty,SecurityDocuments,TypeMonographs,Monographs,Event,TypeEvent,TypeParticipation,TypeGrant,Grant,FormParticipation,NIRS,PopularSciencePublications,FullNameАuthor,ScientificDirections,InternationalCooperation,Department,Faculty,TypeLevel

admin.site.register(UserManager)
admin.site.register(TypePublications)
admin.site.register(Map)
admin.site.register(Publications)
admin.site.register(TypeDocuments)
admin.site.register(TypeProperty)
admin.site.register(SecurityDocuments)
admin.site.register(TypeMonographs)
admin.site.register(Monographs)

admin.site.register(TypeParticipation)
admin.site.register(TypeEvent)
admin.site.register(Event)

admin.site.register(TypeGrant)
admin.site.register(Grant)

admin.site.register(FormParticipation)
admin.site.register(NIRS)

admin.site.register(PopularSciencePublications)

admin.site.register(ScientificDirections)

admin.site.register(FullNameАuthor)

admin.site.register(InternationalCooperation)

admin.site.register(Department)

admin.site.register(Faculty)

admin.site.register(TypeLevel)
# Register your models here.
