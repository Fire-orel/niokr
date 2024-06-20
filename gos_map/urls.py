from django.urls import path
from .views.views import LoginView,HomeView,CheckMap,MapDetails,otchet

from gos_map.views.views_publication import addPublication,deletePublication,editPublication

from gos_map.views.views_security_documents import addSecurityDocuments,deleteSecurityDocuments,editSecurityDocuments

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('chek_map/',CheckMap.as_view(),name='chek_map'),
    path('map_details/<int:pk>',MapDetails.as_view(),name='map_details'),

    path('add_publication/',addPublication.as_view(),name='add_publication'),
    path('edit_publication/<int:pk>/',editPublication.as_view(),name='edit_publication'),
    path('delete_publication/<int:pk>/',deletePublication.as_view(),name='delete_publication'),

    path('add_security_documents/',addSecurityDocuments.as_view(),name='add_security_documents'),
    path('edit_security_documents/<int:pk>/',editSecurityDocuments.as_view(),name='edit_security_documents'),
    path('delete_security_documents/<int:pk>/',deleteSecurityDocuments.as_view(),name='delete_security_documents'),

    path("otchet/", otchet.as_view(), name="otchet")
]
