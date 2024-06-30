from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,FormParticipation
from datetime import datetime

class addFormParticipation(View):
    def post(self, request, *args, **kwargs):

        name_form_participation = request.POST.get("name_form_participation")

        form_participation=FormParticipation.objects.create(
                name_form_participation = name_form_participation
            )
        form_participation.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteFormParticipation(View):
    def post(self, request, pk):
        try:
            form_participation = FormParticipation.objects.get(pk=pk)
            form_participation.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except FormParticipation.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editFormParticipation(View):
    def get(self, request,pk, *args, **kwargs):

        form_participation=get_object_or_404(FormParticipation, id=pk)

        serialized_data = serializers.serialize('json', [form_participation])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        form_participation = get_object_or_404(FormParticipation,id=pk)
        name_form_participation = request.POST.get("name_form_participation")

        form_participation.name_form_participation=name_form_participation

        form_participation.save()



        return JsonResponse({'message': "Success"}, status=200)
