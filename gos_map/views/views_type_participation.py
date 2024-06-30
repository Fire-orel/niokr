from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeParticipation
from datetime import datetime

class addTypeParticipation(View):
    def post(self, request, *args, **kwargs):

        name_type_participation = request.POST.get("name_type_participation")

        type_participation=TypeParticipation.objects.create(
                name_type_participation = name_type_participation
            )
        type_participation.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeParticipation(View):
    def post(self, request, pk):
        try:
            type_participation = TypeParticipation.objects.get(pk=pk)
            type_participation.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeParticipation.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeParticipation(View):
    def get(self, request,pk, *args, **kwargs):

        type_participation=get_object_or_404(TypeParticipation, id=pk)

        serialized_data = serializers.serialize('json', [type_participation])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_participation = get_object_or_404(TypeParticipation,id=pk)
        name_type_participation = request.POST.get("name_type_participation")

        type_participation.name_type_participation=name_type_participation

        type_participation.save()



        return JsonResponse({'message': "Success"}, status=200)
