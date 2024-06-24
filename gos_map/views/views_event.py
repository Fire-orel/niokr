from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeParticipation,TypeEvent,Event
from datetime import datetime

class addEvent(View):
    def post(self, request, *args, **kwargs):
        type_participation = request.POST.get("type_participation")
        full_name_author_event = request.POST.get("full_name_author_event")
        name_event_event = request.POST.get("name_event_event")
        level = request.POST.get("level")
        type_event = request.POST.get("type_event")
        title_report = request.POST.get("title_report")
        date_event_event = request.POST.get("date_event_event")
        place_event = request.POST.get("place_event")
        number_participants = request.POST.get("number_participants")
        number_foreign_participants = request.POST.get("number_foreign_participants")
        number_exhibits = request.POST.get("number_exhibits")
        publication_collection = request.POST.get("publication_collection")
        awards = request.POST.get("awards")
        link = request.POST.get("link")


        status='Редактируется'



        if type_participation!="" and full_name_author_event!="" and name_event_event!="" and level!="" and type_event!="" and title_report!="" and place_event!="" and date_event_event!="" and number_participants!="" and number_foreign_participants!="" and number_exhibits!="" and publication_collection!="" and awards!="" and link!="":
            status="Завершено"

        event=Event.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_participation=TypeParticipation.objects.get(pk=type_participation),
                full_name_author_event=full_name_author_event,
                name_event_event=name_event_event,
                level=level,
                type_event=TypeEvent.objects.get(pk=type_event),
                title_report=title_report,
                date_event_event=date_event_event,
                place_event=place_event,
                number_participants=number_participants,
                number_foreign_participants=number_foreign_participants,
                number_exhibits=number_exhibits,
                publication_collection=publication_collection,
                awards=awards,
                link=link,
                status=status
            )
        event.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteEvent(View):
    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editEvent(View):
    def get(self, request,pk, *args, **kwargs):

        event=get_object_or_404(Event, id=pk)

        serialized_data = serializers.serialize('json', [event])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        event = get_object_or_404(Event,id=pk)
        type_participation = request.POST.get("type_participation")
        full_name_author_event = request.POST.get("full_name_author_event")
        name_event_event = request.POST.get("name_event_event")
        level = request.POST.get("level")
        type_event = request.POST.get("type_event")
        title_report = request.POST.get("title_report")
        date_event_event = request.POST.get("date_event_event")
        place_event = request.POST.get("place_event")
        number_participants = request.POST.get("number_participants")
        number_foreign_participants = request.POST.get("number_foreign_participants")
        number_exhibits = request.POST.get("number_exhibits")
        publication_collection = request.POST.get("publication_collection")
        awards = request.POST.get("awards")
        link = request.POST.get("link")


        status='Редактируется'



        if type_participation!="" and full_name_author_event!="" and name_event_event!="" and level!="" and type_event!="" and title_report!="" and place_event!="" and date_event_event!="" and number_participants!="" and number_foreign_participants!="" and number_exhibits!="" and publication_collection!="" and awards!="" and link!="":
            status="Завершено"

        event.type_participation=TypeParticipation.objects.get(pk=type_participation)
        event.full_name_author_event=full_name_author_event
        event.name_event_event=name_event_event
        event.level=level
        event.type_event=TypeEvent.objects.get(pk=type_event)
        event.title_report=title_report
        event.date_event_event=date_event_event
        event.place_event=place_event
        event.number_participants=number_participants
        event.number_foreign_participants=number_foreign_participants
        event.number_exhibits=number_exhibits
        event.publication_collection=publication_collection
        event.awards=awards
        event.link=link
        event.status=status

        event.save()



        return JsonResponse({'message': "Success"}, status=200)
