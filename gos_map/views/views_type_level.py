from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeLevel
from datetime import datetime

class addTypeLevel(View):
    def post(self, request, *args, **kwargs):

        name_type_level = request.POST.get("name_type_level")

        type_level=TypeLevel.objects.create(
                name_type_level = name_type_level
            )
        type_level.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeLevel(View):
    def post(self, request, pk):
        try:
            type_level = TypeLevel.objects.get(pk=pk)
            type_level.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeLevel.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeLevel(View):
    def get(self, request,pk, *args, **kwargs):

        type_level=get_object_or_404(TypeLevel, id=pk)

        serialized_data = serializers.serialize('json', [type_level])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_level = get_object_or_404(TypeLevel,id=pk)
        name_type_level = request.POST.get("name_type_level")

        type_level.name_type_level=name_type_level

        type_level.save()



        return JsonResponse({'message': "Success"}, status=200)
