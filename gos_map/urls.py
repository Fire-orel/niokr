from django.urls import path
from .views.views import LoginView,HomeView,CheckMap,MapDetails,otchet,mapСompleted,deleteMap,UserDetail,mapReturn

from gos_map.views.views_publication import addPublication,deletePublication,editPublication

from gos_map.views.views_security_documents import addSecurityDocuments,deleteSecurityDocuments,editSecurityDocuments

from gos_map.views.views_monograph import editMonographs,deleteMonograph,addMonographs

from gos_map.views.views_event import addEvent,editEvent,deleteEvent

from gos_map.views.views_grant import addGrant,editGrant,deleteGrant

from gos_map.views.views_nirs import addNIRS,editNIRS,deleteNIRS

from gos_map.views.views_popular_science_publications import addPopularSciencePublications,editPopularSciencePublications,deletePopularSciencePublications

from gos_map.views.views_scientific_directions import addScientificDirections,editScientificDirections,deleteScientificDirections

from gos_map.views.views_international_cooperation import addInternationalCooperation,editInternationalCooperation,deleteInternationalCooperation

from gos_map.views.views_type_publications import addTypePublications,editTypePublications,deleteTypePublications

from gos_map.views.views_type_documents import addTypeDocuments,editTypeDocuments,deleteTypeDocuments

from gos_map.views.views_type_property import addTypeProperty,editTypeProperty,deleteTypeProperty

from gos_map.views.views_type_monographs import addTypeMonographs,editTypeMonographs,deleteTypeMonographs

from gos_map.views.views_type_participation import addTypeParticipation,editTypeParticipation,deleteTypeParticipation

from gos_map.views.views_type_events import addTypeEvent,editTypeEvent,deleteTypeEvent

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('user_detail/', UserDetail.as_view(), name='user_detail'),

    path('map_completed/<int:pk>', mapСompleted.as_view(), name='map_completed'),
    path('map_return/<int:pk>', mapReturn.as_view(), name='map_return'),

    path('chek_map/',CheckMap.as_view(),name='chek_map'),
    path('map_details/<int:pk>',MapDetails.as_view(),name='map_details'),

    path('delete_map/<int:pk>/',deleteMap.as_view(),name='delete_map'),

    path('add_publication/',addPublication.as_view(),name='add_publication'),
    path('edit_publication/<int:pk>/',editPublication.as_view(),name='edit_publication'),
    path('delete_publication/<int:pk>/',deletePublication.as_view(),name='delete_publication'),

    path('add_security_documents/',addSecurityDocuments.as_view(),name='add_security_documents'),
    path('edit_security_documents/<int:pk>/',editSecurityDocuments.as_view(),name='edit_security_documents'),
    path('delete_security_documents/<int:pk>/',deleteSecurityDocuments.as_view(),name='delete_security_documents'),

    path('add_monographs/',addMonographs.as_view(),name='add_monographs'),
    path('edit_monographs/<int:pk>/',editMonographs.as_view(),name='edit_monographs'),
    path('delete_monographs/<int:pk>/',deleteMonograph.as_view(),name='delete_monographs'),

    path('add_event/',addEvent.as_view(),name='add_event'),
    path('edit_event/<int:pk>/',editEvent.as_view(),name='edit_event'),
    path('delete_event/<int:pk>/',deleteEvent.as_view(),name='delete_event'),

    path('add_grant/',addGrant.as_view(),name='add_grant'),
    path('edit_grant/<int:pk>/',editGrant.as_view(),name='edit_grant'),
    path('delete_grant/<int:pk>/',deleteGrant.as_view(),name='delete_grant'),

    path('add_nirs/',addNIRS.as_view(),name='add_nirs'),
    path('edit_nirs/<int:pk>/',editNIRS.as_view(),name='edit_nirs'),
    path('delete_nirs/<int:pk>/',deleteNIRS.as_view(),name='delete_nirs'),

    path('add_popular_science_publications/',addPopularSciencePublications.as_view(),name='add_popular_science_publications'),
    path('edit_popular_science_publications/<int:pk>/',editPopularSciencePublications.as_view(),name='edit_popular_science_publications'),
    path('delete_popular_science_publications/<int:pk>/',deletePopularSciencePublications.as_view(),name='delete_popular_science_publications'),

    path('add_scientific_directions/',addScientificDirections.as_view(),name='add_scientific_directions'),
    path('edit_scientific_directions/<int:pk>/',editScientificDirections.as_view(),name='edit_scientific_directions'),
    path('delete_scientific_directions/<int:pk>/',deleteScientificDirections.as_view(),name='delete_scientific_directions'),

    path('add_international_cooperation/',addInternationalCooperation.as_view(),name='add_international_cooperation'),
    path('edit_international_cooperation/<int:pk>/',editInternationalCooperation.as_view(),name='edit_international_cooperation'),
    path('delete_international_cooperation/<int:pk>/',deleteInternationalCooperation.as_view(),name='delete_international_cooperation'),


    path('add_type_publications/',addTypePublications.as_view(),name='add_type_publications'),
    path('edit_type_publications/<int:pk>/',editTypePublications.as_view(),name='edit_type_publications'),
    path('delete_type_publications/<int:pk>/',deleteTypePublications.as_view(),name='delete_type_publications'),


    path('add_type_documents/',addTypeDocuments.as_view(),name='add_type_documents'),
    path('edit_type_documents/<int:pk>/',editTypeDocuments.as_view(),name='edit_type_documents'),
    path('delete_type_documents/<int:pk>/',deleteTypeDocuments.as_view(),name='delete_type_documents'),



    path('add_type_property/',addTypeProperty.as_view(),name='add_type_property'),
    path('edit_type_property/<int:pk>/',editTypeProperty.as_view(),name='edit_type_property'),
    path('delete_type_property/<int:pk>/',deleteTypeProperty.as_view(),name='delete_type_property'),


    path('add_type_monographs/',addTypeMonographs.as_view(),name='add_type_monographs'),
    path('edit_type_monographs/<int:pk>/',editTypeMonographs.as_view(),name='edit_type_monographs'),
    path('delete_type_monographs/<int:pk>/',deleteTypeMonographs.as_view(),name='delete_type_monographs'),


    path('add_type_participation/',addTypeParticipation.as_view(),name='add_type_participation'),
    path('edit_type_participation/<int:pk>/',editTypeParticipation.as_view(),name='edit_type_participation'),
    path('delete_type_participation/<int:pk>/',deleteTypeParticipation.as_view(),name='delete_type_participation'),


    path('add_type_events/',addTypeEvent.as_view(),name='add_type_events'),
    path('edit_type_events/<int:pk>/',editTypeEvent.as_view(),name='edit_type_events'),
    path('delete_type_events/<int:pk>/',deleteTypeEvent.as_view(),name='delete_type_events'),


    path("otchet/", otchet.as_view(), name="otchet")
]
