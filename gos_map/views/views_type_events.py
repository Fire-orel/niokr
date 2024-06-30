from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeEvent
from datetime import datetime

class addTypeEvent(View):
    def post(self, request, *args, **kwargs):

        name_type_events = request.POST.get("name_type_events")

        type_events=TypeEvent.objects.create(
                name_type_events = name_type_events
            )
        type_events.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeEvent(View):
    def post(self, request, pk):
        try:
            type_events = TypeEvent.objects.get(pk=pk)
            type_events.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeEvent.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeEvent(View):
    def get(self, request,pk, *args, **kwargs):

        type_events=get_object_or_404(TypeEvent, id=pk)

        serialized_data = serializers.serialize('json', [type_events])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_events = get_object_or_404(TypeEvent,id=pk)
        name_type_events = request.POST.get("name_type_events")

        type_events.name_type_events=name_type_events

        type_events.save()



        return JsonResponse({'message': "Success"}, status=200)
