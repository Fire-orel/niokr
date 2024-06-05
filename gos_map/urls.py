from django.urls import path
from .views import LoginView,HomeView,CheckMap,MapDetails,addPublication,deletePublication,otchet

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('chek_map/',CheckMap.as_view(),name='chek_map'),
    path('map_details/<int:pk>',MapDetails.as_view(),name='map_details'),
    path('add_publication/',addPublication.as_view(),name='add_publication'),
    path('delete_publication/<int:pk>/',deletePublication.as_view(),name='delete_publication'),
    path("otchet/", otchet.as_view(), name="otchet")
]
